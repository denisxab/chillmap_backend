import os

default_db = {
    "ENGINE": "django.db.backends.postgresql",
    "NAME": os.environ.get("POSTGRES_DB", "app"),
    "USER": os.environ.get("POSTGRES_USER", "postgres"),
    "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "postgres"),
    "HOST": os.environ.get("POSTGRES_HOST", "db"),
    "PORT": os.environ.get("POSTGRES_PORT", 5432),
}

DATABASES_DEV = {"default": default_db}
