import os
from .base import INSTALLED_APPS, MIDDLEWARE

SECRET_KEY = 'django-insecure-i()o2=lv+0fj6f*=ha=rtuxc!g74$kj&t-q9dhh7i*sm6!+0!q'

DEBUG = True

ALLOWED_HOSTS = ["*"]

CSRF_TRUSTED_ORIGINS = ["https://tunnel.quiznfacts.com"]

# INSTALLED_APPS += ["django_browser_reload"]
INSTALLED_APPS += ["debug_toolbar"]

# MIDDLEWARE += ["django_browser_reload.middleware.BrowserReloadMiddleware"]
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

CORS_ALLOW_ALL_ORIGINS: True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.environ.get("PGDATABASE", "quizbk"),
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

DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

AWS_ACCESS_KEY_ID = '1f8bcff6b47d61799db7beaae02a3fa4'
AWS_SECRET_ACCESS_KEY = '78e32042ccce9896aa5b5767338949146eda472fd532328302be87d2b0ed5260'
AWS_STORAGE_BUCKET_NAME = 'quizzer'
AWS_S3_ENDPOINT_URL = 'https://b46a64eb384beb50a5fc80946bc0abc7.r2.cloudflarestorage.com'
# AWS_S3_PUBLIC_URL = "https://storage.worldstories.net"
AWS_S3_SIGNATURE_VERSION = 's3v4'

# Email Settings
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = "beebayk63478@gmail.com"
EMAIL_HOST_PASSWORD = "eekafahcyhrvgmjx"
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = "beebayk63478@gmail.com"
SERVER_EMAIL = "beebayk63478@gmail.com"