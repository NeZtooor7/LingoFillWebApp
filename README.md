# LingoFill

LingoFill is a Django web application for creating, completing, correcting, saving, and reviewing fill-in-the-blank language exercises.

It supports both AI-generated and manually entered exercises, multilingual interface preferences, persistent user accounts, PostgreSQL-backed exercise history, and profile/language settings.

## Main features

- AI-generated fill-in-the-blank exercises
- Manual fill-in-the-blank exercise creation
- Local answer checking against stored/generated correct answers
- AI explanations for incorrect answers
- PostgreSQL persistence for users, language preferences, exercises, and history
- User registration, login, logout, and persistent sessions
- Account/profile editing
- Preferred interface language per user
- Default learning language per user
- Multiple learning languages per user
- Saved exercise history with detail view
- Exercise title editing and deletion
- Client-side history search and pagination
- Light and dark mode
- DB-driven interface-language availability
- Local static assets for flags and interface resources
- Windows development and local serving with Django, Waitress, and Apache

## Supported interface languages

The current interface supports:

- English (`en`)
- Spanish (`es`)
- German (`de`)
- Japanese (`ja`)
- Hindi (`hi`)
- Romanian (`ro`)
- Italian (`it`)
- Portuguese (`pt`)

Interface-language availability is read from the database. Each enabled language also requires the corresponding frontend resources:

```text
core/static/core/locales/<code>.json
core/static/core/flags/<code>.svg
```

The interface language is independent from the language being learned.

## Architecture

### `core`

Project-wide configuration and shared presentation/infrastructure:

- Django settings
- project URL configuration
- shared base template
- shared CSS and JavaScript
- Alpine components/stores
- i18next language management
- local translation JSON files
- flags and branding assets

### `accounts`

Authentication and user profile concerns:

- custom user model
- registration
- login/logout
- profile editing
- preferred interface language
- default learning language
- user-learning-language relationships
- account-level language context

### `exercises`

Exercise workflow and persistence:

- manual exercise creation
- AI exercise generation
- correction flow
- answer/explanation handling
- exercise persistence
- exercise history
- history detail, title editing, deletion, search, and pagination

### PostgreSQL

PostgreSQL is the durable application database and is accessed through Django/Psycopg 3.

The database stores user/account information, supported languages, user-learning-language relationships, exercises, exercise items, and related history data.

## Technology stack

- Python 3
- Django 5.2
- PostgreSQL
- Psycopg 3
- OpenAI API
- Pydantic
- python-dotenv
- HTML
- CSS
- JavaScript
- Alpine.js
- i18next
- Waitress
- Apache HTTP Server

## Project structure

```text
LingoFillWebApp/
├── accounts/
│   ├── models/
│   ├── templates/accounts/
│   ├── context_processors.py
│   ├── forms.py
│   ├── urls.py
│   └── views.py
├── core/
│   ├── static/core/
│   │   ├── alpine/
│   │   ├── branding/
│   │   ├── flags/
│   │   ├── locales/
│   │   ├── vendor/
│   │   ├── i18n.js
│   │   ├── language-manager.js
│   │   └── styles.css
│   ├── templates/core/
│   │   └── base.html
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── exercises/
│   ├── models/
│   ├── templates/exercises/
│   ├── forms.py
│   ├── llm_service.py
│   ├── urls.py
│   └── views.py
├── staticfiles/
├── .env
├── .env.example
├── manage.py
├── README.md
└── requirements.txt
```

## Environment configuration

Create a `.env` file in the project root. Do not commit real credentials or secrets.

Typical variables used by the current project include:

```env
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=127.0.0.1
DB_PORT=5432

OPENAI_API_KEY=
OPENAI_GENERATION_MODEL=gpt-5-nano
OPENAI_CORRECTION_MODEL=gpt-5-mini
OPENAI_TIMEOUT_SECONDS=45

EXERCISE_SIGNING_SALT=
DJANGO_SECRET_KEY=
```

If the Django secret key is configured from the environment in your current `settings.py`, add its environment variable here as well and keep the real value out of Git.

## PostgreSQL setup

Create a PostgreSQL database and an application user with the permissions required by LingoFill.

Then configure the connection through the `.env` variables above.

Before running the application, verify the database is reachable:

```bash
python manage.py check
```

If the project contains managed migrations, apply them with:

```bash
python manage.py migrate
```

Some project tables may be represented by Django models mapped to an existing PostgreSQL schema. Keep the actual model/schema strategy synchronized with the database before using migration commands that would alter existing tables.

## Installation

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create/configure `.env`, make sure PostgreSQL is running, and then run:

```bash
python manage.py check
python manage.py runserver
```

Use the URL configured by the project URL patterns and shown by the Django development server.

## Authentication and sessions

LingoFill uses Django authentication with the custom `accounts.User` model.

The application supports:

- registration
- login using the configured user identity
- logout
- authenticated-only exercise/history access
- persistent login sessions
- account editing
- preferred interface language
- one or more learning languages
- an optional default learning language

Private exercise/history queries must always be scoped to the authenticated user.

## Exercise workflow

### Manual mode

Manual mode accepts lines containing underscores as blanks.

Example:

```text
- Ich _ müde.
- Du _ glücklich.
```

The app converts each underscore into an input field.

### AI mode

The user describes what they want to practice and can choose exercise options such as:

- learning language
- CEFR level
- sentence count
- blanks
- grammar focus
- verbs
- subjects
- tense
- topic
- expressions

The server generates a structured exercise and keeps API credentials server-side.

### Correction

Correct answers are checked against the generated/stored answer data. Incorrect answers can receive AI-generated explanations in the selected interface language.

### Saving and history

Authenticated users can save exercises and revisit them through Exercise History.

History supports:

- reverse-chronological saved exercises
- title
- creation date/time
- learning language
- detail view
- title editing
- deletion
- client-side search
- configurable items per page
- pagination

History access must always enforce ownership through `request.user`.

## Interface language behavior

The interface language and learning language are separate settings.

The preferred interface language is stored on the user account. Supported interface-language codes are provided from the database to the frontend, and i18next loads the matching locale JSON file.

Changing interface language must not silently change the user's learning language.

## Static files and branding

Shared static files belong under:

```text
core/static/core/
```

Branding assets should live under:

```text
core/static/core/branding/
```

For production-like local serving, collect static files:

```bash
python manage.py collectstatic
```

## Running with Waitress

From the project root, the current Django project module is `core`, so the WSGI target is:

```text
core.wsgi:application
```

Example:

```powershell
.\.venv\Scripts\waitress-serve.exe --listen=127.0.0.1:8001 core.wsgi:application
```

## Running through Apache on Windows

A local production-like flow can use:

```text
Browser → Apache → Waitress → Django
```

Apache can reverse-proxy application requests to Waitress and serve collected static assets from `staticfiles/`.

Keep Apache-specific paths and proxy rules in deployment/local-server documentation rather than hard-coding them into Django application logic.

## Security notes

- Never commit `.env`.
- Never expose OpenAI API keys to browser JavaScript or templates.
- Never store plain-text passwords.
- Use Django password hashing/authentication APIs.
- Validate persistent/security-sensitive values on the backend even when Alpine/JavaScript also validates them.
- Scope private exercise/history operations to `request.user`.
- Use POST + CSRF protection for mutating actions such as logout and deletion.
- Keep Django secret keys and signing salts outside source control.

## Development checks

Before considering a change complete, run:

```bash
python manage.py check
```

Then manually test at least:

- registration
- login
- logout
- persistent session behavior
- account editing
- preferred interface language
- default learning language
- manual exercise creation
- AI exercise generation
- correction
- saving
- history list/detail
- title editing
- deletion
- history search/pagination
- dark/light mode
- all supported interface languages

## Known limitations / next steps

- A database language entry still needs the matching locale JSON and flag asset before it can be used correctly by the frontend.
- AI functionality requires a configured API key and network access.
- Local Apache/Waitress deployment configuration is environment-specific.
- Automated test coverage can be expanded further as the project evolves.

## License

This project is intended for educational and portfolio use unless a different license is added to the repository.
