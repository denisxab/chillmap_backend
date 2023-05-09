import os
from pathlib import Path

#
BASE_DIR = Path(__file__).resolve().parent.parent
#
DATABASES_POSTGRES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB", "app"),
        "USER": os.environ.get("POSTGRES_USER", "postgres"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "postgres"),
        "HOST": os.environ.get("POSTGRES_HOST", "db"),
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
    }
}
DATABASES_SQLITE = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
DATABASES_SELECT = DATABASES_POSTGRES
#
ALLOWED_HOSTS_SELECT = ["*"]
#
SECRET_KEY_SELECT = "django-insecure-ah3y)b6&1l_&$#v4k8%oui3c!5l=81985j5k6lp&!17k^2raur"
#
DEBUG_SELECT = True
#
