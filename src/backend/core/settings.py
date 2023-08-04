import ast
import os
from pathlib import Path

import dj_database_url
import django_cache_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


def get_list(text):
    return [item.strip() for item in text.split(",")]


def get_bool_from_env(name, default_value):
    if name in os.environ:
        value = os.environ[name]
        try:
            return ast.literal_eval(value)
        except ValueError as e:
            raise ValueError("{} is an invalid value for {}".format(value, name)) from e
    return default_value


USE_ACCOUNT_APP = get_bool_from_env("USE_ACCOUNT_APP", True)
USE_TAG_APP = get_bool_from_env("USE_TAG_APP", True)
USE_FORUM_APP = get_bool_from_env("USE_FORUM_APP", True)

ACCOUNT_SERVICE_URL = os.environ.get(
    "ACCOUNT_SERVICE_URL", "http://localhost:8000/api/"
)
TAG_SERVICE_URL = os.environ.get("TAG_SERVICE_URL", "http://localhost:8000/api/")
FORUM_SERVICE_URL = os.environ.get("FORUM_SERVICE_URL", "http://localhost:8000/api/")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY", "secret")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = get_bool_from_env("DEBUG", True)

ALLOWED_HOSTS = get_list(
    os.environ.get(
        "ALLOWED_HOSTS",
        "localhost,0.0.0.0,127.0.0.1,udpt-account-django,udpt-tag-django,udpt-forum-django",
    )
)

# Application definition
INSTALLED_APPS = [
    "django.contrib.staticfiles",
    "corsheaders",
]

if USE_ACCOUNT_APP:
    INSTALLED_APPS += [
        "django.contrib.contenttypes",
        "django.contrib.auth",
        "account",
    ]

if USE_TAG_APP and not USE_ACCOUNT_APP:
    INSTALLED_APPS += ["django.contrib.contenttypes"]

if USE_TAG_APP:
    INSTALLED_APPS += ["taggit"]

if USE_FORUM_APP:
    INSTALLED_APPS += ["forum"]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = "core.urls"

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

WSGI_APPLICATION = "core.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
DATABASE_URL_ENV_NAME = os.environ.get("DATABASE_URL_ENV_NAME", "DATABASE_URL")

DATABASES = {
    "default": dj_database_url.config(
        env=DATABASE_URL_ENV_NAME,
        default="sqlite:///:memory:",
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_ROOT = BASE_DIR / "static"

STATIC_URL = "static/"

MEDIA_ROOT = BASE_DIR / "media"

MEDIA_URL = "media/"

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
        "OPTIONS": {
            "location": MEDIA_ROOT,
            "base_url": MEDIA_URL,
        },
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        "OPTIONS": {
            "location": STATIC_ROOT,
            "base_url": STATIC_URL,
        },
    },
}

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CORS_ALLOW_ALL_ORIGINS = True

# caches
CACHES = {"default": django_cache_url.config()}

CACHEOPS_ENABLED = os.environ.get("CACHEOPS_ENABLED", False)

if CACHEOPS_ENABLED:
    CACHEOPS_REDIS = os.environ.get("CACHEOPS_REDIS", "redis://localhost:6379/0")

    CACHEOPS = {
        "*.*": {"ops": "all", "timeout": 60 * 15},
        "migrations.*": {"ops": (), "timeout": 0},
    }

if USE_ACCOUNT_APP:
    AUTH_USER_MODEL = "account.User"

    AUTHENTICATION_BACKENDS = [
        "account.backends.JWTBackend",
        "django.contrib.auth.backends.ModelBackend",
    ]
