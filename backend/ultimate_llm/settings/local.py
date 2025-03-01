# settings/local.py

# ======== IMPORTS ========
from ultimate_llm.settings.base import get_secret

from .base import *

# ======== DEBUG SETTINGS ========
DEBUG = True

# ======== DATABASE CONFIGURATION ========
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": get_secret("DATABASE_NAME"),
        "USER": get_secret("DATABASE_USER"),
        "PASSWORD": get_secret("DATABASE_PASSWORD"),
        "HOST": get_secret("HOST"),
        "PORT": "5432",
    }
}

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    # "http://localhost:5173/*",
    "http://*",
]

CORS_ALLOW_ALL_ORIGINS = True
