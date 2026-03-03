"""
Test settings for integration tests.

Uses SQLite in-memory so the test suite can run without an Oracle connection.
Oracle-specific migrations (migration 0003 — sequences/triggers) are bypassed
by setting MIGRATION_MODULES = {'coreRelback': None}, which causes Django to
create the app's tables directly from model definitions (syncdb-style) instead
of running the Oracle-only RunSQL operations.

Usage:
    DJANGO_SETTINGS_MODULE=projectRelback.settings_test python manage.py test coreRelback.tests
"""
from projectRelback.settings_dev import *  # noqa: F401, F403

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Bypass Oracle-specific migration 0003 (sequences/triggers).
# Django will build coreRelback tables directly from model definitions.
# auth and contenttypes use their standard SQLite-compatible migrations.
MIGRATION_MODULES = {
    'coreRelback': None,
}
