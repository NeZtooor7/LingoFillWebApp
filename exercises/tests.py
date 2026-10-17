from unittest.mock import Mock, patch

from django.test import RequestFactory, SimpleTestCase
from django.urls import reverse

from accounts.models.user import User
from . import views
from .forms import AIExerciseRequestForm
from .llm_service import build_ai_generation_request


class ExerciseOptionsTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User(id=7, preferred_interface_language_id=1, default_learning_language_id=2)
        self.user.save = Mock()
        self.data = dict(
            ai_goal='Practice German', level='B2', sentence_count='20',
            blank_count='2-3', focus=['verbs', 'tenses'],
            learning_language='de', spoken_language='en',
        )

        languages = patch.object(views.Languages.objects, 'filter').start()
        languages.return_value.first.return_value = Mock(code='de')
        links = patch.object(views.UsersLearningLanguages.objects, 'filter').start()
        links.return_value.select_related.return_value.order_by.return_value = []
        patch.object(views.Languages.objects, 'order_by', return_value=[]).start()
        self.addCleanup(patch.stopall)

    def request(self, data=None):
        url = reverse('exercises:ai_exercise_create')
        request = self.factory.get('/') if data is None else self.factory.post(url, data)
        request.user = self.user
        request.session = {}
        return request

    def test_b2_and_focus_are_valid_generation_options(self):
        form = AIExerciseRequestForm(self.data)
        self.assertTrue(form.is_valid(), form.errors)
        generation_request = build_ai_generation_request(form.cleaned_data)
        self.assertEqual(generation_request['level'], 'B2')
        self.assertEqual(generation_request['sentence_count'], 20)
        self.assertEqual(generation_request['blanks_per_sentence'], '2-3')
        self.assertEqual(generation_request['focus'], ['verbs', 'tenses'])

    def test_invalid_options_remain_rejected_on_submission(self):
        for option, value in (
            ('level', 'C2'), ('sentence_count', '999'),
            ('blank_count', '4'), ('focus', ['unrecognized']),
        ):
            with self.subTest(option=option):
                form = AIExerciseRequestForm({**self.data, option: value})
                self.assertFalse(form.is_valid())
                self.assertIn(option, form.errors)

    def test_home_has_defaults_without_saving_account_options(self):
        context = views._home_context(self.request())
        self.assertEqual(context['ai_form']['level'].value(), 'A1')
        self.assertEqual(context['ai_form']['sentence_count'].value(), '10')
        self.assertEqual(context['ai_form']['blank_count'].value(), '1')
        self.assertFalse(context['exercise_options_bound'])
        self.assertEqual(context['initial_learning_language_code'], 'de')
        self.user.save.assert_not_called()

    def test_bound_options_take_precedence_after_an_error(self):
        bound = AIExerciseRequestForm(self.data)
        context = views._home_context(self.request(), ai_form=bound, errors=['Invalid goal'])
        self.assertIs(context['ai_form'], bound)
        self.assertTrue(context['exercise_options_bound'])
        self.assertEqual(context['ai_form']['level'].value(), 'B2')
        self.assertEqual(context['ai_form']['sentence_count'].value(), '20')
        self.assertEqual(context['ai_form']['blank_count'].value(), '2-3')
        self.assertEqual(context['ai_form']['focus'].value(), ['verbs', 'tenses'])
        self.assertEqual(context['errors'], ['Invalid goal'])
        self.user.save.assert_not_called()

    def test_generation_errors_render_submitted_options(self):
        errors = (
            views.LLMConfigurationError('API configuration unavailable'),
            views.LLMGenerationError('Unexpected AI response'),
            RuntimeError('Unavailable'),
        )
        for error in errors:
            with (
                self.subTest(error=type(error).__name__),
                patch.object(views, 'generate_ai_exercise', side_effect=error),
                patch.object(views, 'render', side_effect=lambda request, template, context: context),
            ):
                context = views.ai_exercise_create(self.request(self.data))
                self.assertTrue(context['exercise_options_bound'])
                self.assertEqual(context['ai_form']['level'].value(), 'B2')
                self.assertEqual(context['ai_form']['focus'].value(), ['verbs', 'tenses'])
                self.assertTrue(context['errors'])
        self.user.save.assert_not_called()
