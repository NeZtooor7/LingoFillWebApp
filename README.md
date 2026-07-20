# LingoFill

**LingoFill** is a local-first Django web app for creating AI-assisted fill-in-the-blank language exercises.

The app supports two workflows:

1. **AI mode** (default) — describe what you want to practice, choose the exercise language, level, number of sentences, blanks, and grammar focus. The app generates a structured fill-in-the-blank exercise using an LLM API.
2. **Manual mode** — paste your own sentences using underscores (`_`) and turn them into an interactive exercise.

LingoFill is designed for language learning, grammar drills, vocabulary practice, verb conjugation, and personalized cloze-style exercises.

---

## Features

- Add other supported languages like Chinese, French, Arabic, Russian, Persian, Afrikaans, Korean, Quechua, etc.
- AI-generated fill-in-the-blank exercises
- Manual fill-in-the-blank exercise creation
- Multiple blanks per sentence
- Multiple sentences per exercise
- Local answer checking against generated `correct_answers`
- AI explanations only for incorrect answers
- Correction results page with correct and wrong matches
- Separate **interface language** and **exercise language**
- Multilingual interface
- Exercise language selector
- Light/dark mode, with dark mode as the default
- Flag-based language dropdowns
- Custom multiselect field for grammar focus
- Clipboard support for completed manual exercises
- Input validation for manual sentence format
- Local-first design
- Windows support with Waitress and Apache reverse proxy

---

## Supported Interface Languages

The webpage interface can be displayed in:

- Spanish
- English
- German
- Japanese
- Hindi
- Romanian
- Italian
- Portuguese

The **interface language** is also used as the explanation language for correction feedback.

---

## Supported Exercise Languages

The AI exercise generator can create exercises in:

- Spanish
- English
- German
- Japanese
- Hindi
- Romanian
- Italian
- Portuguese

The **exercise language** is independent from the interface language.

Example:

- Interface language: English
- Exercise language: German
- Result: German exercises with English explanations

Another example:

- Interface language: Portuguese
- Exercise language: Japanese
- Result: Japanese exercises with Portuguese explanations

---

## How It Works

### AI Mode

The user enters a goal such as:

```text
Practice sein and haben in present tense with ich, du, er, sie and wir.
```

Then the user selects:

- Exercise language
- Level
- Number of sentences
- Number of blanks
- Focus areas such as verbs, articles, pronouns, tenses, or expressions
- Optional advanced fields such as verbs, subjects, tense, topic, and expressions

The app sends a structured request to the LLM API and expects a structured response.

The generated response contains:

- Exercise title
- Language
- Level
- Instructions
- Sentence templates
- Full completed sentences
- Blank metadata
- Correct answers
- Grammar focus

Example structure:

```json
{
  "exercise_title": "Present tense practice",
  "language": "German",
  "level": "A1",
  "instructions": "Complete the sentences with the correct word.",
  "sentences": [
    {
      "number": 1,
      "template": "- Ich _ müde.",
      "full_sentence": "Ich bin müde.",
      "blanks": [
        {
          "position": 1,
          "correct_answers": ["bin"],
          "grammar_focus": "sein, present tense, ich"
        }
      ]
    }
  ]
}
```

### Correction Flow

When the user submits an AI-generated exercise:

1. Django checks the user's answers locally.
2. If an answer matches one of the `correct_answers`, it is marked as correct.
3. If an answer does not match, only the wrong blank is sent to the correction model.
4. The correction model explains the mistake in the selected interface language.
5. The correction results page shows:
   - User sentence
   - Correct sentence
   - Correct matches
   - Wrong answers
   - Correct answers
   - AI explanations for mistakes

This keeps API usage low because correct answers do not require an extra model call.

---

## Manual Mode

Manual mode accepts plain text input.

Each line must:

1. Start with `- `
2. Contain at least one underscore `_`
3. Have text before and after the blank

Valid example:

```text
- Ich _ müde.
- Du _ glücklich.
- Er _ zu Hause.
```

The app turns each underscore into a text input.

Example exercise:

```text
1. Ich [____] müde.
2. Du [____] glücklich.
3. Er [____] zu Hause.
```

After filling the blanks with `bin`, `bist`, and `ist`, the clipboard output becomes:

```text
1. Ich bin müde.
2. Du bist glücklich.
3. Er ist zu Hause.
```

---

## Tech Stack

- Python
- Django
- OpenAI API
- Pydantic
- python-dotenv
- HTML
- CSS
- JavaScript
- Waitress
- Apache HTTP Server
- WhiteNoise

---

## Requirements

- Python 3.10+
- Django 5.x
- OpenAI Python SDK
- Pydantic
- python-dotenv
- Waitress
- WhiteNoise

Install dependencies with:

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root.

```env
OPENAI_API_KEY=your-real-api-key-here

OPENAI_GENERATION_MODEL=gpt-5-nano
OPENAI_CORRECTION_MODEL=gpt-5-mini

OPENAI_TIMEOUT_SECONDS=45
```

The recommended budget-friendly setup is:

- `gpt-5-nano` for exercise generation
- `gpt-5-mini` for correction explanations

Correct answers are checked locally first. The correction model is only called for wrong answers. You can copy and paste from the `.env.example` the structure of your new `.env` file and replace the values of the keys with what you need.

Never commit your real `.env` file.

---

## `.gitignore`

Recommended entries:

```gitignore
.env
db.sqlite3
__pycache__/
*.pyc
staticfiles/
.venv/
```

---

## Local Development Setup

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it.

### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

### Windows CMD

```cmd
.venv\Scripts\activate.bat
```

### macOS/Linux

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the development server:

```bash
python manage.py runserver
```

Open the app:

```text
http://127.0.0.1:8000/LingoFillWebApp/
```

---

## Static Files

During development with `runserver`, Django serves static files automatically.

For Apache/Waitress usage, collect static files:

```bash
python manage.py collectstatic
```

This copies files from:

```text
exercises/static/
```

to:

```text
staticfiles/
```

---

## Running with Waitress

From the project root:

```powershell
.\.venv\Scripts\waitress-serve.exe --listen=127.0.0.1:8001 fillblanker.wsgi:application
```

Then open:

```text
http://127.0.0.1:8001/LingoFillWebApp/
```

The WSGI import target is:

```text
fillblanker.wsgi:application
```

---

## Running with Apache on Windows

This project can be served locally through Apache using a reverse proxy.

Expected final URL:

```text
http://localhost/LingoFillWebApp/
```

General flow:

```text
Browser → Apache → Waitress → Django
```

Apache forwards:

```text
/LingoFillWebApp/
```

to Waitress running at:

```text
http://127.0.0.1:8001/LingoFillWebApp/
```

Static files can be served by Apache from:

```text
staticfiles/
```

After changing CSS or JavaScript, run:

```bash
python manage.py collectstatic
```

Then restart Apache/Waitress if needed.

---

## Suggested Project Structure

```text
LingoFill/
├── exercises/
│   ├── static/
│   │   └── exercises/
│   │       ├── flags/
│   │       ├── clipboard.js
│   │       ├── i18n.js
│   │       ├── learning_language.js
│   │       ├── multiselect.js
│   │       ├── styles.css
│   │       └── theme.js
│   ├── templates/
│   │   └── exercises/
│   │       ├── base.html
│   │       ├── correction_results.html
│   │       ├── exercise.html
│   │       └── home.html
│   ├── forms.py
│   ├── llm_schemas.py
│   ├── llm_service.py
│   ├── urls.py
│   └── views.py
├── fillblanker/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── staticfiles/
├── .env.example
├── .gitignore
├── manage.py
├── README.md
└── requirements.txt
```

---

## Important Design Notes

### No database required for core usage

LingoFill does not need a database for the main exercise flow.

Generated exercise data can be signed and sent back through the form for correction, avoiding the need to store exercises in a database.

### API keys stay server-side

The OpenAI API keys are used only in Django/Python.

They must never be placed in:

- HTML templates
- JavaScript files
- GitHub commits
- Browser code

### Manual mode works without an API key

Manual mode does not require OpenAI API access.

This makes the project usable even without paid API usage.

### AI mode requires an API key

AI exercise generation and AI explanations require OpenAI API access.

---

## Development Workflow

While coding:

```bash
python manage.py runserver
```

Use:

```text
http://127.0.0.1:8000/LingoFillWebApp/
```

After changing static files and testing with Apache/Waitress:

```bash
python manage.py collectstatic
```

For local production-like testing:

```powershell
.\.venv\Scripts\waitress-serve.exe --listen=127.0.0.1:8001 fillblanker.wsgi:application
```

Use:

```text
http://localhost/LingoFillWebApp/
```

if Apache is configured as a reverse proxy.

---

## Possible Future Improvements

- Mock AI mode for offline testing
- Export exercises as PDF
- Save exercise templates
- Add hints
- Add keyboard shortcuts
- Add user-created exercise collections
- Add progress tracking
- Add Docker support
- Add unit tests for schema validation and correction logic
- Add dynamic placeholders based on selected exercise language

---

## License

This project is intended for educational and portfolio purposes.
