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
