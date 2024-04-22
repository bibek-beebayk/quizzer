import os
from .base import INSTALLED_APPS, MIDDLEWARE

SECRET_KEY = "django-insecure-i()o2=lv+0fj6f*=ha=rcuxc!g74$kj&t-q9dhh7i*sm6!+0!q"

DEBUG = False

ALLOWED_HOSTS = ["quizzer-production-35fb.up.railway.app", "quiz.bibek0001.com.np"]

CSRF_TRUSTED_ORIGINS = ["https://quizzer-production-35fb.up.railway.app", "https:quiz.bibek0001.com.np"]

DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

AWS_ACCESS_KEY_ID = "1f8bcff6b47d61799db7beaae02a3fa4"
AWS_SECRET_ACCESS_KEY = (
    "78e32042ccce9896aa5b5767338949146eda472fd532328302be87d2b0ed5260"
)
AWS_STORAGE_BUCKET_NAME = "bonewa"
AWS_S3_ENDPOINT_URL = (
    "https://b46a64eb384beb50a5fc80946bc0abc7.r2.cloudflarestorage.com/bonewa"
)
AWS_S3_SIGNATURE_VERSION = "s3v4"

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

MIDDLEWARE += [
    "whitenoise.middleware.WhiteNoiseMiddleware",
]
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="https://a5888a2b1232e5d70b297e00f1f97023@o4505908028702720.ingest.us.sentry.io/4507084460589056",
    integrations=[DjangoIntegration()],
    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
    environment="quiz",
)