"""
Local development settings — SQLite file DB + Demo Mode.

Use this when you don't have Oracle available but want to run the full
web interface with realistic fake data.

Usage:
    DJANGO_SETTINGS_MODULE=projectRelback.settings_local python manage.py migrate
    DJANGO_SETTINGS_MODULE=projectRelback.settings_local python manage.py seed_demo
    DJANGO_SETTINGS_MODULE=projectRelback.settings_local python manage.py runserver
"""
from projectRelback.settings_dev import *  # noqa: F401, F403

# File-based SQLite (persists between server restarts)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Bypass Oracle-specific migrations (sequences/triggers — not supported by SQLite)
MIGRATION_MODULES = {
    "coreRelback": None,
}

# Demo mode: OracleRmanRepository is replaced by DemoRmanRepository in views.
# This populates the Reports and Log Detail pages with realistic fixture data.
DEMO_MODE = True
ORACLE_CATALOG = None
