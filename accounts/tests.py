import json
from types import SimpleNamespace
from unittest.mock import Mock, patch

from django.contrib.auth.models import AnonymousUser
from django.test import Client, RequestFactory, SimpleTestCase
from django.urls import reverse

from . import views
from .forms import AccountEditForm, RegistrationForm
from .models.languages import Languages
from .models.user import User


class NicknameFormTests(SimpleTestCase):
    def nickname_form(self, form_class, value, duplicate=False):
        user = User(id=7, preferred_interface_language_id=1)
        with (
            patch.object(Languages.objects, "order_by", return_value=Languages.objects.none()),
            patch("accounts.forms.get_user_model") as get_user_model,
        ):
            queryset = get_user_model.return_value.objects.filter.return_value
            queryset.exists.return_value = duplicate
            queryset.exclude.return_value.exists.return_value = duplicate
            kwargs = {"user": user} if form_class is AccountEditForm else {}
            form = form_class(data={"nickname": value}, **kwargs)
            # Other required fields are intentionally absent; check nickname alone.
            form.is_valid()
        return form, queryset

    def test_valid_nicknames_are_lowercased_in_both_forms(self):
        for form_class in (RegistrationForm, AccountEditForm):
            for nickname in ("Abcd", "a123", "Player42", "Z" + "9" * 149):
                with self.subTest(form=form_class.__name__, nickname=nickname):
                    form, _ = self.nickname_form(form_class, nickname)
                    self.assertNotIn("nickname", form.errors)
                    self.assertEqual(form.cleaned_data["nickname"], nickname.lower())

    def test_invalid_nicknames_are_rejected_before_uniqueness_lookup(self):
        invalid = (
            "", "abc", "1234", "1abc", "_abc", "abc_", "ab-c", "ab.c",
            "ab c", " abcd", "abcd ", "abc\t", "abcd\n", "ábcd", "aébc",
            "Ａbcd", "abc١", "Nick😀", "a" * 151,
        )
        for form_class in (RegistrationForm, AccountEditForm):
            for nickname in invalid:
                with self.subTest(form=form_class.__name__, nickname=nickname):
                    form, queryset = self.nickname_form(form_class, nickname)
                    self.assertIn("nickname", form.errors)
                    self.assertNotIn("nickname", form.cleaned_data)
                    queryset.exists.assert_not_called()
                    queryset.exclude.assert_not_called()

    def test_case_insensitive_duplicates_are_still_rejected(self):
        for form_class in (RegistrationForm, AccountEditForm):
            with self.subTest(form=form_class.__name__):
                form, queryset = self.nickname_form(form_class, "Player42", duplicate=True)
                self.assertIn("This nickname is already in use.", form.errors["nickname"])
                if form_class is AccountEditForm:
                    queryset.exclude.assert_called_once_with(id=7)


class LanguagePreferenceViewTests(SimpleTestCase):
    endpoints = (
        ("set_interface_language", "preferred_interface_language_id"),
        ("set_learning_language", "default_learning_language_id"),
    )

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User(
            id=7,
            preferred_interface_language_id=1,
            default_learning_language_id=2,
        )
        self.user.save = Mock()

    def request(self, name, data=None, method="post", user=None):
        request = getattr(self.factory, method)(
            reverse(f"accounts:{name}"), data=data or {}
        )
        request.user = self.user if user is None else user
        return getattr(views, name)(request)

    def test_each_preference_saves_only_its_own_field(self):
        for name, field_name in self.endpoints:
            with self.subTest(endpoint=name):
                self.user.preferred_interface_language_id = 1
                self.user.default_learning_language_id = 2
                self.user.save.reset_mock()
                with patch.object(views.Languages.objects, "filter") as languages:
                    languages.return_value.first.return_value = SimpleNamespace(
                        id=3, code="pt"
                    )
                    response = self.request(name, {"language_code": "pt"})

                self.assertEqual(response.status_code, 200)
                self.assertEqual(json.loads(response.content), {"language_code": "pt"})
                languages.assert_called_once_with(code="pt")
                self.user.save.assert_called_once_with(update_fields=[field_name])
                self.assertEqual(getattr(self.user, field_name), 3)
                other_field = (
                    "default_learning_language_id"
                    if field_name == "preferred_interface_language_id"
                    else "preferred_interface_language_id"
                )
                self.assertEqual(
                    getattr(self.user, other_field),
                    2 if other_field == "default_learning_language_id" else 1,
                )

    def test_invalid_or_missing_language_does_not_save(self):
        for name, _ in self.endpoints:
            for code in (None, "", "xx", "EN", " en ", "x" * 11):
                with self.subTest(endpoint=name, language_code=code):
                    with patch.object(views.Languages.objects, "filter") as languages:
                        languages.side_effect = lambda **kwargs: SimpleNamespace(
                            first=lambda: (
                                SimpleNamespace(id=1, code="en")
                                if kwargs["code"] == "en"
                                else None
                            )
                        )
                        response = self.request(
                            name, {} if code is None else {"language_code": code}
                        )

                    self.assertEqual(response.status_code, 400)
                    self.assertEqual(
                        json.loads(response.content), {"error": "Invalid language."}
                    )
                    self.user.save.assert_not_called()
                    self.assertEqual(self.user.preferred_interface_language_id, 1)
                    self.assertEqual(self.user.default_learning_language_id, 2)

    def test_anonymous_requests_return_json_without_looking_up_languages(self):
        for name, _ in self.endpoints:
            with self.subTest(endpoint=name):
                with patch.object(views.Languages.objects, "filter") as languages:
                    response = self.request(
                        name, {"language_code": "en"}, user=AnonymousUser()
                    )

                self.assertEqual(response.status_code, 401)
                self.assertEqual(
                    json.loads(response.content),
                    {"error": "Authentication required."},
                )
                self.assertNotIn("Location", response)
                languages.assert_not_called()

    def test_only_post_is_allowed(self):
        for name, _ in self.endpoints:
            for method in ("get", "head", "put", "patch", "delete"):
                with self.subTest(endpoint=name, method=method):
                    with patch.object(views.Languages.objects, "filter") as languages:
                        response = self.request(name, method=method)

                    self.assertEqual(response.status_code, 405)
                    self.assertEqual(response.headers["Allow"], "POST")
                    languages.assert_not_called()
                    self.user.save.assert_not_called()

    def test_csrf_protection_is_retained(self):
        client = Client(enforce_csrf_checks=True)
        for name, _ in self.endpoints:
            with self.subTest(endpoint=name):
                response = client.post(
                    reverse(f"accounts:{name}"), {"language_code": "en"}
                )
                self.assertEqual(response.status_code, 403)
