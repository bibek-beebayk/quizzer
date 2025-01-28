import os
from .base import INSTALLED_APPS, MIDDLEWARE

SECRET_KEY = 'django-insecure-i()o2=lv+0fj6f*=ha=rtuxc!g74$kj&t-q9dhh7i*sm6!+0!q'

DEBUG = True

ALLOWED_HOSTS = ["*"]

CSRF_TRUSTED_ORIGINS = ["https://erp-tunnel.kalodhunga.com"]

# INSTALLED_APPS += ["django_browser_reload"]
INSTALLED_APPS += ["debug_toolbar"]

# MIDDLEWARE += ["django_browser_reload.middleware.BrowserReloadMiddleware"]
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.environ.get("PGDATABASE", "quiz"),
        "USER": os.environ.get("PGUSER", "postgres"),
        "PASSWORD": os.environ.get("PGPASSWORD", ""),
        "HOST": os.environ.get("PGHOST", ""),
        "PORT": os.environ.get("PGPORT", ""),
        "ATOMIC_REQUESTS": True,
    }
}

INTERNAL_IPS = [
    "127.0.0.1",
]

# LOGGING = {
#     "version": 1,
#     "handlers": {
#         "console": {
#             "class": "logging.StreamHandler",
#         },
#     },
#     "loggers": {
#         "django.db.backends": {
#             "level": "DEBUG",
#             "handlers": ["console"],
#         },
#     },
# }