import json
from unittest.mock import Mock, patch

from django.contrib.auth.models import AnonymousUser
from django.test import Client, RequestFactory, SimpleTestCase
from django.urls import reverse

from accounts.models.user import User
from . import views
from .forms import AIExerciseRequestForm, ExercisePreferenceForm
from .llm_service import build_ai_generation_request


class ExercisePreferenceTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User(id=7, preferred_interface_language_id=1, default_learning_language_id=2)
        self.user.save = Mock()
        self.url = reverse('exercises:set_exercise_preference')

    def request(self, data, user=None):
        request = self.factory.post(self.url, data)
        request.user = self.user if user is None else user
        return views.set_exercise_preference(request)

    def test_each_option_updates_only_its_own_field(self):
        for option, value in [('level', 'B2'), ('sentence_count', '30'), ('blank_count', '2-3')]:
            with self.subTest(option=option):
                previous = {
                    key: getattr(self.user, key)
                    for key in ('exercise_level', 'exercise_sentence_count', 'exercise_blank_count',
                                'default_learning_language_id', 'preferred_interface_language_id')
                }
                self.user.save.reset_mock()
                response = self.request({'option': option, 'value': value, 'user_id': 999})
                field = f'exercise_{option}'
                self.assertEqual(response.status_code, 200)
                self.assertEqual(json.loads(response.content), {'option': option, 'value': value})
                self.assertEqual(str(getattr(self.user, field)), value)
                self.user.save.assert_called_once_with(update_fields=[field])
                for key, previous_value in previous.items():
                    if key != field:
                        self.assertEqual(getattr(self.user, key), previous_value)

    def test_invalid_options_do_not_save(self):
        for data in ({}, {'option': 'nickname', 'value': 'hacked'},
                     {'option': 'level', 'value': 'C2'}, {'option': 'level', 'value': 'b2'},
                     {'option': 'sentence_count', 'value': '999'},
                     {'option': 'sentence_count', 'value': '-1'},
                     {'option': 'blank_count', 'value': '4'},
                     {'option': 'level', 'value': ''}):
            with self.subTest(data=data):
                self.assertEqual(self.request(data).status_code, 400)
                self.user.save.assert_not_called()

    def test_authentication_post_and_csrf_are_required(self):
        response = self.request({'option': 'level', 'value': 'B2'}, user=AnonymousUser())
        self.assertEqual(response.status_code, 401)
        self.assertNotIn('Location', response)
        for method in ('get', 'put', 'patch', 'delete'):
            request = getattr(self.factory, method)(self.url)
            request.user = self.user
            self.assertEqual(views.set_exercise_preference(request).status_code, 405)
        self.assertEqual(Client(enforce_csrf_checks=True).post(
            self.url, {'option': 'level', 'value': 'B2'}
        ).status_code, 403)
        self.user.save.assert_not_called()

    def test_b2_is_valid_for_generation_and_preferences(self):
        data = dict(ai_goal='Practice German', level='B2', sentence_count='10',
                    blank_count='1-2', learning_language='de', spoken_language='en')
        form = AIExerciseRequestForm(data)
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data['level'], 'B2')
        self.assertEqual(build_ai_generation_request(form.cleaned_data)['level'], 'B2')
        self.assertTrue(ExercisePreferenceForm({'option': 'level', 'value': 'B2'}).is_valid())

    def test_home_restores_account_values_and_keeps_bound_values_on_errors(self):
        self.user.exercise_level = 'B2'
        self.user.exercise_sentence_count = 20
        self.user.exercise_blank_count = '2-3'
        request = self.factory.get('/')
        request.user = self.user
        request.session = {}
        with (
            patch.object(views.Languages.objects, 'order_by', return_value=[]),
            patch.object(views.Languages.objects, 'filter') as languages,
            patch.object(views.UsersLearningLanguages.objects, 'filter') as links,
        ):
            languages.return_value.first.return_value = Mock(code='de')
            links.return_value.select_related.return_value.order_by.return_value = []
            context = views._home_context(request)
            self.assertEqual(context['ai_form']['level'].value(), 'B2')
            self.assertEqual(context['ai_form']['sentence_count'].value(), '20')
            self.assertEqual(context['ai_form']['blank_count'].value(), '2-3')
            bound = AIExerciseRequestForm({'level': 'A2', 'sentence_count': '5', 'blank_count': '1'})
            context = views._home_context(request, ai_form=bound, errors=['Invalid goal'])
            self.assertIs(context['ai_form'], bound)
            self.assertEqual(context['ai_form']['level'].value(), 'A2')
        self.user.save.assert_not_called()
