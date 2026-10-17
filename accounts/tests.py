import json
from types import SimpleNamespace
from unittest.mock import Mock, patch

from django.contrib.auth.models import AnonymousUser
from django.test import Client, RequestFactory, SimpleTestCase
from django.urls import reverse

from . import views
from .models.user import User


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
