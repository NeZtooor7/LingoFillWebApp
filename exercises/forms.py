import re
from django import forms


LINE_PATTERN = re.compile(r"^- .+_.+$")


class SentenceInputForm(forms.Form):
    source_text = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'rows': 12,
                'placeholder': '- Ich _ müde.\n- Du _ glücklich.\n- Er _ zu Hause.',
                'class': 'sentence-textarea',
            }
        ),
    )

    def clean_source_text(self):
        source_text = self.cleaned_data['source_text']

        lines = [line.strip() for line in source_text.splitlines() if line.strip()]

        if not lines:
            raise forms.ValidationError('Please write at least one sentence.')

        errors = []

        for index, line in enumerate(lines, start=1):
            if not line.startswith('- '):
                errors.append(f'Line {index}: must start with "- ".')
                continue

            if '_' not in line:
                errors.append(f'Line {index}: must contain at least one underscore "_".')
                continue

            if not LINE_PATTERN.match(line):
                errors.append(f'Line {index}: must contain text before and after the underscore.')

        if errors:
            raise forms.ValidationError(errors)

        return '\n'.join(lines)


class AIExerciseRequestForm(forms.Form):
    LEVEL_CHOICES = [
        ('A1', 'A1'),
        ('A2', 'A2'),
        ('B1', 'B1'),
        ('B2', 'B2'),
    ]

    SENTENCE_COUNT_CHOICES = [
        ('5', '5'),
        ('10', '10'),
        ('15', '15'),
        ('20', '20'),
        ('30', '30'),
    ]

    BLANK_COUNT_CHOICES = [
        ('1', '1 blank'),
        ('1-2', '1–2 blanks'),
        ('2-3', '2–3 blanks'),
    ]

    FOCUS_CHOICES = [
        ('verbs', 'Verbs'),
        ('articles', 'Articles'),
        ('pronouns', 'Pronouns'),
        ('tenses', 'Tenses'),
        ('expressions', 'Expressions'),
    ]

    TENSE_CHOICES = [
        ('', 'Auto'),
        ('present', 'Present'),
        ('past', 'Past'),
        ('perfect', 'Perfect'),
        ('future', 'Future'),
        ('conditional', 'Conditional'),
    ]

    LANGUAGE_CHOICES = [
        ('es', 'Spanish'),
        ('en', 'English'),
        ('de', 'German'),
        ('ja', 'Japanese'),
        ('hi', 'Hindi'),
        ('ro', 'Romanian'),
        ('it', 'Italian'),
        ('pt', 'Portuguese'),
    ]

    ai_goal = forms.CharField(
        required=True,
        max_length=800,
    )

    level = forms.ChoiceField(
        choices=LEVEL_CHOICES,
        required=True,
    )

    sentence_count = forms.ChoiceField(
        choices=SENTENCE_COUNT_CHOICES,
        required=True,
    )

    blank_count = forms.ChoiceField(
        choices=BLANK_COUNT_CHOICES,
        required=True,
    )

    focus = forms.MultipleChoiceField(
        choices=FOCUS_CHOICES,
        required=False,
    )

    verbs = forms.CharField(
        required=False,
        max_length=250,
    )

    subjects = forms.CharField(
        required=False,
        max_length=250,
    )

    tense = forms.ChoiceField(
        choices=TENSE_CHOICES,
        required=False,
    )

    topic = forms.CharField(
        required=False,
        max_length=250,
    )

    expressions = forms.CharField(
        required=False,
        max_length=300,
    )

    learning_language = forms.ChoiceField(
        choices=LANGUAGE_CHOICES,
        required=True,
    )

    spoken_language = forms.ChoiceField(
        choices=LANGUAGE_CHOICES,
        required=True,
    )

    def clean_sentence_count(self):
        return int(self.cleaned_data['sentence_count'])
