
from django.contrib.auth.decorators import login_required
from django.core import signing
from django.conf import settings
from django.db import transaction
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST

from .models import Exercises, ExerciseItems
from .forms import AIExerciseRequestForm, SentenceInputForm
from accounts.models.languages import Languages
from accounts.models.users_learning_languages import UsersLearningLanguages
from .llm_service import (
    LLMConfigurationError,
    LLMGenerationError,
    explain_wrong_answers,
    generate_ai_exercise,
)


from .models import Exercises, ExerciseItems

@login_required
@ensure_csrf_cookie
def home(request):
    all_languages = list(Languages.objects.order_by('id'))
    forced_learning_language_code = request.session.pop('force_learning_language_code_once', None)
    learning_language_links = (UsersLearningLanguages.objects
        .filter(user=request.user)
        .select_related('language')
        .order_by('language__id'))

    registered_learning_languages = [link.language for link in learning_language_links]
    show_learning_language_dialog = False
    force_default_learning_language = request.session.pop('force_default_learning_language_once', False)
    force_preferred_interface_language = request.session.pop('force_preferred_interface_language_once', False)

    if request.user.default_learning_language_id is None:
        if len(registered_learning_languages) == 1:
            default_language = registered_learning_languages[0]
            request.user.default_learning_language_id = default_language.id
            request.user.save(update_fields=['default_learning_language_id'])
            forced_learning_language_code = default_language.code
        elif len(registered_learning_languages) > 1:
            show_learning_language_dialog = True
    default_learning_language = None

    if request.user.default_learning_language_id is not None:
        default_learning_language = (Languages.objects
            .filter(id=request.user.default_learning_language_id)
            .first())

    initial_learning_language_code = (forced_learning_language_code
            or (default_learning_language.code if default_learning_language else 'en'))
    force_default_learning_language = (forced_learning_language_code is not None)

    return render(
        request,
        'exercises/home.html',
        {
            'form': SentenceInputForm(),
            'ai_form': AIExerciseRequestForm(),
            'all_languages': all_languages,
            'registered_learning_languages': registered_learning_languages,
            'show_learning_language_dialog': show_learning_language_dialog,
            'default_learning_language': default_learning_language,
            'force_default_learning_language': force_default_learning_language,
            'force_preferred_interface_language': force_preferred_interface_language,
            'initial_learning_language_code': initial_learning_language_code,
        },
    )


def build_sentence_chunks(source_text):
    sentences = []

    lines = [
        line.strip()
        for line in source_text.splitlines()
        if line.strip()
    ]

    for number, line in enumerate(lines, start=1):
        clean_line = line[2:] if line.startswith('- ') else line
        parts = clean_line.split('_')
        chunks = []
        blank_position = 0

        for index, part in enumerate(parts):
            show_input_after = index < len(parts) - 1

            chunk = {
                'text': part,
                'show_input_after': show_input_after,
            }

            if show_input_after:
                blank_position += 1
                chunk['blank_position'] = blank_position

            chunks.append(chunk)

        sentences.append(
            {
                'number': number,
                'chunks': chunks,
            }
        )

    return sentences


@login_required
def manual_exercise_create(request):
    if request.method != 'POST':
        return redirect('core:home')

    form = SentenceInputForm(request.POST)

    if not form.is_valid():
        return render(
            request,
            'exercises/home.html',
            {
                'form': form,
                'ai_form': AIExerciseRequestForm(),
            },
        )

    source_text = form.cleaned_data['source_text']
    sentences = build_sentence_chunks(source_text)

    return render(
        request,
        'exercises/exercise.html',
        {
            'sentences': sentences,
            'source_text': source_text,
            'exercise_mode': 'manual',
        },
    )


@login_required
def ai_exercise_create(request):
    if request.method != 'POST':
        return redirect('core:home')

    ai_form = AIExerciseRequestForm(request.POST)

    if not ai_form.is_valid():
        return render(
            request,
            'exercises/home.html',
            {
                'form': SentenceInputForm(),
                'ai_form': ai_form,
                'errors': ai_form.errors.values(),
            },
        )

    try:
        generated_exercise = generate_ai_exercise(ai_form.cleaned_data)
    except LLMConfigurationError as error:
        return render(
            request,
            'exercises/home.html',
            {
                'form': SentenceInputForm(),
                'ai_form': ai_form,
                'errors': [str(error)],
            },
        )
    except LLMGenerationError as error:
        return render(
            request,
            'exercises/home.html',
            {
                'form': SentenceInputForm(),
                'ai_form': ai_form,
                'errors': [str(error), 'Please try again. The AI response did not match the expected exercise structure.'],
            },
        )
    except Exception:
        return render(
            request,
            'exercises/home.html',
            {
                'form': SentenceInputForm(),
                'ai_form': ai_form,
                'errors': ['The AI exercise could not be generated right now. Please check your API key, internet connection, and model name.'],
            },
        )

    generated_exercise_data = generated_exercise.model_dump()
    generated_exercise_data['learning_language_code'] = ai_form.cleaned_data['learning_language']
    generated_exercise_data['spoken_language_code'] = ai_form.cleaned_data['spoken_language']
    generated_exercise_data["ai_prompt"] = (
            ai_form.cleaned_data.get("ai_goal", "").strip()
            or None
    )

    generated_exercise_data["generation_settings"] = {
        "level": ai_form.cleaned_data.get("level"),
        "sentence_count": ai_form.cleaned_data.get("sentence_count"),
        "blank_count": ai_form.cleaned_data.get("blank_count"),
        "focus": ai_form.cleaned_data.get("focus") or [],
        "spoken_language_code": ai_form.cleaned_data.get("spoken_language"),
    }

    advanced_options = {
        key: ai_form.cleaned_data.get(key)
        for key in ("verbs", "subjects", "tense", "topic", "expressions")
        if ai_form.cleaned_data.get(key)
    }

    generated_exercise_data["advanced_options"] = advanced_options or None
    generated_exercise_data["started_at"] = timezone.now().isoformat()
    source_text = '\n'.join(sentence['template'] for sentence in generated_exercise_data['sentences'])
    signed_exercise_data = signing.dumps(generated_exercise_data)
    sentences = build_sentence_chunks(source_text)

    return render(
        request,
        'exercises/exercise.html',
        {
            'sentences': sentences,
            'source_text': source_text,
            'exercise_mode': 'ai',
            'signed_exercise_data': signed_exercise_data,
            'generated_exercise': generated_exercise_data,
        },
    )


def normalize_answer(value):
    return ' '.join(value.strip().casefold().split())


def answer_is_correct(user_answer, correct_answers):
    normalized_user_answer = normalize_answer(user_answer)

    return normalized_user_answer in {
        normalize_answer(correct_answer)
        for correct_answer in correct_answers
    }


def build_user_sentence(template, answers_by_position):
    clean_template = template[2:] if template.startswith('- ') else template
    parts = clean_template.split('_')
    final_sentence = ''

    for index, part in enumerate(parts):
        final_sentence += part

        position = index + 1

        if position < len(parts):
            final_sentence += answers_by_position.get(position, '')

    return final_sentence

def build_saved_exercise_results(exercise):
    items = (ExerciseItems.objects
        .filter(exercise_id=exercise.id)
        .order_by("position"))
    results = []
    correct_count = 0
    total_blanks = 0

    for item in items:
        correct_answers_by_position = {int(entry["position"]): entry.get("answers", []) for entry in (item.correct_answers or [])}
        submitted_answers_by_position = {int(entry["position"]): entry.get("answer", "") for entry in (item.submitted_answers or [])}
        blank_results = []

        for position in sorted(correct_answers_by_position):
            correct_answers = correct_answers_by_position[position]
            user_answer = submitted_answers_by_position.get(position, "")
            is_correct = answer_is_correct(user_answer, correct_answers)
            total_blanks += 1

            if is_correct:
                correct_count += 1

            blank_results.append({
                "position": position,
                "user_answer": user_answer,
                "correct_answers": correct_answers,
                "is_correct": is_correct,
            })
        correct_sentence_answers = {
            position: answers[0] if answers else ""
            for position, answers
                in correct_answers_by_position.items()
        }

        results.append({
            "number": item.position,
            "user_sentence": build_user_sentence(item.sentence_template, submitted_answers_by_position),
            "correct_sentence": build_user_sentence(item.sentence_template, correct_sentence_answers),
            "sentence_is_correct": all(blank["is_correct"] for blank in blank_results),
            "blanks": blank_results,
            "explanation": item.explanation,
        })
    return {
        "results": results,
        "correct_count": correct_count,
        "total_blanks": total_blanks,
        "wrong_count": total_blanks - correct_count,
    }

@login_required
def ai_exercise_correct(request):
    if request.method != 'POST':
        return redirect('core:home')

    signed_exercise_data = request.POST.get('signed_exercise_data', '')

    try:
        generated_exercise = signing.loads(signed_exercise_data, max_age=60 * 60 * 6)
    except signing.BadSignature:
        return render(
            request,
            'exercises/home.html',
            {
                'form': SentenceInputForm(),
                'ai_form': AIExerciseRequestForm(),
                'errors': ['The exercise data could not be verified. Please generate the exercise again.'],
            },
        )

    results = []
    wrong_blanks_for_ai = []
    correct_count = 0
    total_blanks = 0

    for sentence in generated_exercise['sentences']:
        sentence_number = sentence['number']
        answers_by_position = {}
        blank_results = []

        for blank in sentence['blanks']:
            blank_position = blank['position']
            input_name = f'answer_{sentence_number}_{blank_position}'
            user_answer = request.POST.get(input_name, '').strip()
            correct_answers = blank['correct_answers']

            is_correct = answer_is_correct(user_answer, correct_answers)

            total_blanks += 1

            if is_correct:
                correct_count += 1
            else:
                wrong_blanks_for_ai.append(
                    {
                        'sentence_number': sentence_number,
                        'template': sentence['template'],
                        'full_sentence': sentence['full_sentence'],
                        'blank_position': blank_position,
                        'user_answer': user_answer,
                        'correct_answers': correct_answers,
                        'grammar_focus': blank.get('grammar_focus', ''),
                    }
                )

            answers_by_position[blank_position] = user_answer

            blank_results.append(
                {
                    'position': blank_position,
                    'user_answer': user_answer,
                    'correct_answers': correct_answers,
                    'is_correct': is_correct,
                    'grammar_focus': blank.get('grammar_focus', ''),
                    'explanation': '',
                }
            )

        results.append(
            {
                'number': sentence_number,
                'template': sentence['template'],
                'correct_sentence': sentence['full_sentence'],
                'user_sentence': build_user_sentence(sentence['template'], answers_by_position),
                'sentence_is_correct': all(blank_result['is_correct'] for blank_result in blank_results),
                'blanks': blank_results,
            }
        )

    explanations_by_blank = {}

    if wrong_blanks_for_ai:
        try:
            explanations_by_blank = explain_wrong_answers(
                generated_exercise=generated_exercise,
                wrong_blanks=wrong_blanks_for_ai,
            )
        except Exception:
            explanations_by_blank = {}

    for sentence_result in results:
        for blank_result in sentence_result['blanks']:
            key = (
                sentence_result['number'],
                blank_result['position'],
            )

            if key in explanations_by_blank:
                blank_result['explanation'] = explanations_by_blank[key]

    save_exercise_data = {
        "generated_exercise": generated_exercise,
        "results": results,
        "completed_at": timezone.now().isoformat()
    }
    signed_save_exercise_data = signing.dumps(save_exercise_data, salt=settings.EXERCISE_SIGNING_SALT)

    return render(
        request,
        'exercises/correction_results.html',
        {
            'results': results,
            'correct_count': correct_count,
            'total_blanks': total_blanks,
            'wrong_count': total_blanks - correct_count,
            "signed_save_exercise_data": signed_save_exercise_data,
        },
    )

@login_required
@require_POST
def save_corrected_exercise(request):
    signed_data = request.POST.get("signed_save_exercise_data", "")

    try:
        save_data = signing.loads(signed_data, salt=settings.EXERCISE_SIGNING_SALT, max_age=60 * 60 * 6)
    except signing.BadSignature:
        return HttpResponseBadRequest("The exercise data could not be verified.")

    generated_exercise = save_data.get("generated_exercise", {})
    results = save_data.get("results", [])
    total_blanks = sum(len(sentence["blanks"]) for sentence in results)
    correct_count = sum(
        1
        for sentence in results
            for blank in sentence["blanks"]
                if blank["is_correct"])
    context = {
        "results": results,
        "correct_count": correct_count,
        "total_blanks": total_blanks,
        "wrong_count": total_blanks - correct_count,
        "signed_save_exercise_data": signed_data,
    }

    try:
        learning_language = (Languages.objects
            .filter(code=generated_exercise.get("learning_language_code"))
            .first())

        if learning_language is None or not results:
            raise ValueError("The exercise data is incomplete.")

        with transaction.atomic():
            exercise = Exercises.objects.create(
                user                = request.user,
                learning_language   = learning_language,
                source              = "ai",
                title               = generated_exercise.get("exercise_title" or None),
                generation_settings = generated_exercise.get("generation_settings"),
                ai_prompt           = generated_exercise.get("ai_prompt"),
                advanced_options    = generated_exercise.get("advanced_options"),
                started_at          = parse_datetime(generated_exercise.get("started_at", "")) or timezone.now(),
                completed_at        = parse_datetime(save_data.get("completed_at","")) or timezone.now(),
            )
            exercise_items = []

            for sentence in results:
                blanks = sentence["blanks"]
                correct_answers = [{"position": blank["position"], "answers": blank["correct_answers"]} for blank in blanks]
                submitted_answers = [{"position": blank["position"], "answer": blank["user_answer"]} for blank in blanks]
                wrong_blanks = [blank for blank in blanks if not blank["is_correct"]]
                explanation = None

                if wrong_blanks:
                    explanation_parts = []
                    for blank in wrong_blanks:
                        explanation_text = blank.get("explanation") or "No AI explanation was available."

                        if len(wrong_blanks) == 1:
                            explanation_parts.append(explanation_text)
                        else:
                            explanation_parts.append(f'Blank {blank["position"]}: {explanation_text}')
                    explanation = "\n\n".join(explanation_parts)
                exercise_items.append(ExerciseItems(
                    exercise          = exercise,
                    position          = sentence["number"],
                    sentence_template = sentence["template"],
                    correct_answers   = correct_answers,
                    submitted_answers = submitted_answers,
                    explanation       = explanation,
                ))
            ExerciseItems.objects.bulk_create(exercise_items)
        context["save_success"] = True

    except Exception:
        context["save_error"] = True

    return render(request, "exercises/correction_results.html", context)

@login_required
def exercise_history(request):
    exercises = (Exercises.objects
        .filter(user_id=request.user.id)
        .select_related("learning_language")
        .order_by("-created_at"))

    return render(request, "exercises/exercise_history.html", {"exercises": exercises})

@login_required
def exercise_history_detail(request, exercise_id):
    exercise = get_object_or_404(Exercises.objects.select_related("learning_language"),
        id=exercise_id,
        user_id=request.user.id)
    correction_data = build_saved_exercise_results(exercise)
    raw_advanced_options = (exercise.advanced_options or {})
    option_definitions = (("verbs", "verbsLabel"), ("subjects", "subjectsLabel"), ("tense", "tenseLabel"),
            ("topic", "topicLabel"), ("expressions", "expressionsLabel"))
    advanced_options = []

    for option_name, label_key in option_definitions:
        value = raw_advanced_options.get(option_name)
        if not value:
            continue
        if isinstance(value, list):
            value = ", ".join(str(item) for item in value)
        advanced_options.append({"label_key": label_key, "value": value})

    return render(
        request,
        "exercises/exercise_history_detail.html",
        {
            "exercise": exercise,
            "advanced_options": advanced_options,
            **correction_data,
        },
    )

@login_required
@require_POST
def edit_exercise_title(request, exercise_id):
    exercise = get_object_or_404(Exercises, id=exercise_id, user_id=request.user.id)
    title = request.POST.get("title", "").strip()
    exercise.title = title[:255] or None
    exercise.save(update_fields=["title"])

    return redirect("exercises:exercise_history")

@login_required
@require_POST
def delete_exercise(request, exercise_id):
    exercise = get_object_or_404(Exercises, id=exercise_id, user_id=request.user.id)
    exercise.delete()

    return redirect("exercises:exercise_history")