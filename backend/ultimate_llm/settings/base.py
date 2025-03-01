"""
Django settings for ultimate_llm project.

Generated by 'django-admin startproject' using Django 5.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see https://docs.djangoproject.com/en/5.1/ref/settings/
"""

# ======== IMPORTS ========
from pathlib import Path
from typing import Any

import environ
from django.core.exceptions import ImproperlyConfigured

# ======== BASE SETTINGS ========
BASE_DIR = Path(__file__).parents[2]
SETTINGS_DIR = BASE_DIR / "ultimate_llm" / "settings"
TEMP_DIR = BASE_DIR / "temp"
MEDIA_ROOT = TEMP_DIR / "UploadedFiles"

# Initialize environment variable handling
env = environ.Env()
env.read_env(BASE_DIR / ".env")


# ======== SECRETS MANAGEMENT ========
def get_secret(key: str, default: Any = None) -> Any:
    """
    Retrieve secrets from the .env file. If the key is not found,
    return the default value if provided, otherwise raise an exception.
    """
    try:
        # Attempt to retrieve the secret
        return env(key)
    except KeyError:
        if default is None:
            raise ImproperlyConfigured(f"Missing environment variable: {key}")
        return default
    except FileNotFoundError:
        raise ImproperlyConfigured(".env file not found in the project directory.")


SECRET_KEY = get_secret("SECRET_KEY")

# ======== SECURITY SETTINGS ========
DEBUG = False
ALLOWED_HOSTS = ["*"]

# ======== APPLICATION SETTINGS ========
INSTALLED_APPS = [
    "oauth2_provider",
    "rest_framework",
    "corsheaders",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "users",
    "document_parser",
    "llm_chat",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "ultimate_llm.urls"
WSGI_APPLICATION = "ultimate_llm.wsgi.application"
ASGI_APPLICATION = "ultimate_llm.asgi.application"

# ======== AUTHENTICATION ========
AUTH_USER_MODEL = "users.User"
LOGIN_URL = "/admin/login/"

# ======== CHANNELS CONFIGURATION ========
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    }
}

# ======== AUTHENTICATION & PASSWORD VALIDATION ========
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]
OAUTH2_PROVIDER = {
    "SCOPES": {
        "read": "Read scope",
        "write": "Write scope",
        "groups": "Access to your groups",
    },
    "ACCESS_TOKEN_EXPIRE_SECONDS": 3600,  # Token expires in 1 hour
    "REFRESH_TOKEN_EXPIRE_SECONDS": 1209600,  # Refresh token expires in 14 days
}


# ======== DJANGO REST FRAMEWORK CONFIGURATION ========
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "oauth2_provider.contrib.rest_framework.OAuth2Authentication",
    ),
}

# ======== TEMPLATES CONFIGURATION ========
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ======== INTERNATIONALIZATION ========
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"  # GMT +5:30
USE_I18N = True
USE_TZ = True

# ======== STATIC FILES ========
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"
STATICFILES_DIRS = [
    BASE_DIR / "ultimate_llm" / "static",
]
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# ======== DEFAULT PRIMARY KEY FIELD TYPE ========
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ======== ENVIROMENT VARIABLES ========
# OPENAI_API_KEY = get_secret("OPENAI_API_KEY")
