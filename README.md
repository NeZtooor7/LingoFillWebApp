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
├── database/
│   ├── schema.sql
│   └── seed_languages.sql
├── staticfiles/
├── .env
├── .env.example
├── compose.yaml
├── Dockerfile
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

DJANGO_ALLOWED_HOSTS=
DJANGO_CSRF_TRUSTED_ORIGINS=
```

If the Django secret key is configured from the environment in your current `settings.py`, add its environment variable here as well and keep the real value out of Git.

## PostgreSQL setup

Use either your existing PostgreSQL installation or the Docker database described below. For an existing installation, create a PostgreSQL database and an application user with the permissions required by LingoFill.

Then configure the connection through the `.env` variables above.

Check the Django configuration, then verify the connection using a database client:

```bash
python manage.py check
```

`manage.py check` checks project configuration; it does not prove that PostgreSQL is reachable or that its schema is installed.

The application models map to existing tables using `managed = False`. The supplied `database/schema.sql` also creates Django's built-in tables. See the migration-history note in the Docker instructions before applying Django migrations to a database restored from this file.

## Docker database alternative

Docker runs a separate PostgreSQL server for local development. You can use it instead of installing PostgreSQL directly on your computer, or alongside an existing installation. Your original database and its data remain separate; this setup does not copy them.

The root `Dockerfile` builds a PostgreSQL 17.11 image. On the first startup of an empty database volume, PostgreSQL runs these files in order:

1. `database/schema.sql` creates the complete exported schema, including application tables, Django tables, sequences, constraints, indexes, functions, triggers, and comments.
2. `database/seed_languages.sql` adds the eight supported interface languages so registration and language selection have their required reference data.

The schema export contains no users, exercises, sessions, or other existing records. Docker runs the database; continue running Django from your Python environment as described under Installation.

### Install Docker

On Windows, install [Docker Desktop](https://docs.docker.com/desktop/setup/install/windows-install/) and follow its WSL 2 requirements. Start Docker Desktop and use Linux containers. Docker Desktop includes Docker Compose.

On Linux, install [Docker Engine](https://docs.docker.com/engine/install/) and the [Docker Compose plugin](https://docs.docker.com/compose/install/linux/). Start the Docker daemon and ensure your user can run Docker commands. Docker Desktop is also available for macOS and Linux.

Verify the installation in PowerShell or your terminal:

```bash
docker version
docker compose version
```

`docker version` must show both a client and a server. These instructions use Compose v2 (`docker compose`).

### Configure the connection

Run all commands below from the project root, the folder containing `manage.py` and `compose.yaml`. Create `.env` only if you do not already have one.

Windows PowerShell:

```powershell
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
```

Linux/macOS:

```bash
if [ ! -f .env ]; then cp .env.example .env; fi
```

The `.env.example` template already uses these Docker connection defaults. Edit them in `.env` as needed, replacing the password placeholder with your own password:

```env
DB_NAME=lingofill
DB_USER=lingofill_user
DB_PASSWORD=replace-with-your-local-database-password
DB_HOST=127.0.0.1
DB_PORT=5434
```

Keep your existing Django and OpenAI settings in the same file. Docker Compose and Django both read this `.env`; changing the connection selects which database the application uses.

Port `5434` on your computer forwards to PostgreSQL's port `5432` inside the container. This lets a native PostgreSQL installation keep using its usual port. If `5434` is occupied, choose another unused `DB_PORT` and use it in your database client too. The published port binds to `127.0.0.1` for access from your computer.

### Start and use the database

```bash
docker compose up -d --build --wait
docker compose ps
docker compose logs db
```

The first command builds the image, starts PostgreSQL in the background, and waits for the database health check. Look for successful execution of both initialization scripts in the logs. If startup fails, inspect `docker compose logs db` before trying again.

Open a PostgreSQL terminal inside the container without installing PostgreSQL tools on your computer:

```bash
docker compose exec db psql -U lingofill_user -d lingofill
```

Use the `DB_USER` and `DB_NAME` you configured if they differ from this example. In `psql`, run `\dt public.*` to list tables, `SELECT code, name FROM languages ORDER BY code;` to see the seeded languages, and `\q` to exit.

You can also connect using free Navicat Lite with a PostgreSQL connection:

| Setting | Value |
| --- | --- |
| Host | `127.0.0.1` |
| Port | `5434`, or your chosen `DB_PORT` |
| Database | Your `DB_NAME` |
| User | Your `DB_USER` |
| Password | Your `DB_PASSWORD` |
| SSL | Disabled for this local container |

Schema initialization is handled by Docker and PostgreSQL, so no paid Navicat export or import features are required.

With your Python environment activated and dependencies installed, run Django against the container:

```bash
python manage.py check
python manage.py runserver
```

**Django migrations:** this schema-only dump includes the `django_migrations` table but none of its migration-history rows. It also contains no content-type or permission records. Django may report unapplied migrations even though their tables already exist. Do not run `manage.py migrate`, `--fake`, or `--fake-initial` blindly against this restored schema: migration history must first be reconciled with the actual schema and the project's migration files. Restore verified matching migration records or establish an explicitly reviewed migration baseline before applying future migrations or relying on populated Django admin permissions.

### Stop, restart, and preserve data

```bash
docker compose stop
docker compose start
```

Alternatively, `docker compose down` removes the containers and network while retaining the named `postgres_data` volume. Run `docker compose up -d --wait` to recreate the container with the same data.

The initialization SQL runs **only when the PostgreSQL volume is empty**. Rebuilding the image after changing `schema.sql` does not update an existing database. Changing `DB_NAME`, `DB_USER`, or `DB_PASSWORD` in `.env` also does not change databases, roles, or passwords already stored in that volume. Keep matching connection settings, make deliberate changes through PostgreSQL, or reset an expendable development database.

### Reset an expendable development database

The following command permanently deletes this Compose project's database volume, including all accounts, exercises, and other records stored in it. Back up anything you need first. It does not delete your separate native PostgreSQL database.

```bash
docker compose down --volumes
docker compose up -d --build --wait
```

This recreates the database using the current schema, seed file, and `.env` credentials. It is a reset, not a schema upgrade.

### Export an updated schema

To export the Docker database's structure without installing `pg_dump` locally, write the file inside the container and copy it to the project:

```bash
docker compose exec db pg_dump -U lingofill_user -d lingofill --schema-only --no-owner --no-privileges --file=/tmp/lingofill_schema.sql
docker compose cp db:/tmp/lingofill_schema.sql database/schema.sql
```

If exporting your native database instead, run its compatible `pg_dump`, adjusting these connection details:

```bash
pg_dump -h 127.0.0.1 -p 5432 -U lingofill_user -d lingofill -W --schema-only --no-owner --no-privileges --file=database/schema.sql
```

Both exports replace `database/schema.sql`; review the changes before committing. A schema-only export does not include the reference-language seed or Django migration-history rows.

This configuration is intended for local development. The official PostgreSQL image creates `DB_USER` as its bootstrap administrator; use separate, limited application roles and appropriate credentials for a production deployment.


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
