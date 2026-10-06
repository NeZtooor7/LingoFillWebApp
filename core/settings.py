import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
DEBUG = True
ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ["DJANGO_ALLOWED_HOSTS"].split(",")
    if host.strip()
]

AUTH_USER_MODEL = "accounts.User"

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "accounts.apps.AccountsConfig",
    "exercises.apps.ExercisesConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.environ["DJANGO_CSRF_TRUSTED_ORIGINS"].split(",")
    if origin.strip()
]

SECURE_PROXY_SSL_HEADER = (
    "HTTP_X_FORWARDED_PROTO",
    "https",
)

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",

        "DIRS": [
            BASE_DIR / "core" / "templates",
        ],

        "APP_DIRS": True,

        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "accounts.context_processors.user_language_preferences",
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ["DB_NAME"],
        "USER": os.environ["DB_USER"],
        "PASSWORD": os.environ["DB_PASSWORD"],
        "HOST": os.environ.get("DB_HOST", "127.0.0.1"),
        "PORT": os.environ.get("DB_PORT", "5432"),
    }
}

LANGUAGE_CODE = 'en'

USE_I18N = True

LANGUAGES = [
    ('es', 'Español'),
    ('en', 'English'),
    ('de', 'Deutsch'),
    ('ja', '日本語'),
    ('hi', 'हिन्दी'),
    ('ro', 'Română'),
    ('it', 'Italiano'),
    ('pt', 'Português'),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

TIME_ZONE = 'Europe/Berlin'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / "core" / "static",
]

STATIC_ROOT = BASE_DIR / 'staticfiles'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = "accounts:login"
LOGIN_REDIRECT_URL = "exercises:home"
LOGOUT_REDIRECT_URL = "accounts:login"

SESSION_COOKIE_AGE = 28 * 24 * 60 * 60
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
OPENAI_GENERATION_MODEL = os.getenv('OPENAI_GENERATION_MODEL', 'gpt-5-nano')
OPENAI_CORRECTION_MODEL = os.getenv('OPENAI_CORRECTION_MODEL', 'gpt-5-mini')
OPENAI_TIMEOUT_SECONDS = int(os.getenv('OPENAI_TIMEOUT_SECONDS', '45'))

EXERCISE_SIGNING_SALT = os.getenv("EXERCISE_SIGNING_SALT")

if not EXERCISE_SIGNING_SALT:
    raise RuntimeError("EXERCISE_SIGNING_SALT is not configured.")