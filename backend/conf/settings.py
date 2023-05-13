import logging
import os
import sys

from .settings_local import (
    ALLOWED_HOSTS_SELECT,
    BASE_DIR,
    DATABASES_SELECT,
    DEBUG_SELECT,
    HOST_SRERVER_STATIC,
    SECRET_KEY_SELECT,
)


if "pytest" in sys.argv[0] or "test" in sys.argv:
    """Настройки при тестирование"""
    DEBUG_SELECT = False


SERVER_VERSION = "0.0.3"

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = SECRET_KEY_SELECT

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = DEBUG_SELECT

ALLOWED_HOSTS = ALLOWED_HOSTS_SELECT

LOG_DIR = BASE_DIR / "log"
LOG_DIR.mkdir(exist_ok=True)

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "rest_framework",
    "django_filters",
    "api",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "conf.urls"

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

WSGI_APPLICATION = "conf.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = DATABASES_SELECT


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "ru"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = f"{HOST_SRERVER_STATIC}static_django/"
STATIC_ROOT = BASE_DIR / "static"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

ASGI_APPLICATION = "asgi.application"

if DEBUG:
    # Всегда показывать панель с отладкой
    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TOOLBAR_CALLBACK": lambda request: True,
    }
    INSTALLED_APPS.append("debug_toolbar")
    MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")


# Логировать все SQL запросы
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "str": {
            "format": "[{name}-{levelname}] {asctime} {module} {pathname}:> {message}",
            "style": "{",
        },
        "json": {
            "format": '{{"name": "{name}", "levelname": "{levelname}", "asctime": "{asctime}", "module": "{module}", "pathname": "{pathname}", "message": "{message}", "server": "%s"}}'
            % (os.environ["IP_ADR"],),
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "str",
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": str(LOG_DIR / "logfile_sql.log"),
            "formatter": "json",
        },
    },
    "loggers": {
        "django.db.backends": {
            "handlers": [
                "file",  # "console"
            ],
            "level": "DEBUG" if DEBUG else "INFO",
        },
        "djangocore": {
            "handlers": ["console", "file"],
            "level": "INFO",
        },
        "api": {
            "handlers": ["console", "file"],
            "level": "INFO",
        },
    },
}
# Логгер который используется в API
logger_api = logging.getLogger("api")
# Логгер который используется для общей логики Django
logger_djangocore = logging.getLogger("djangocore")


print("Settings: ", dict(DEBUG=DEBUG))
