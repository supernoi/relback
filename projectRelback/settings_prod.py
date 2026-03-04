"""
Production settings for relback.

Differences from base settings.py:
  - DEBUG = False
  - SECRET_KEY required from env (DJANGO_SECRET_KEY)
  - ALLOWED_HOSTS from env (comma-separated)
  - WhiteNoise serves compressed static files
  - Database from env (DB_ENGINE / DB_NAME / …) — falls back to SQLite demo mode
  - django_browser_reload removed
  - Container-friendly structured logging to stdout

Usage:
    export DJANGO_SETTINGS_MODULE=projectRelback.settings_prod
    export DJANGO_SECRET_KEY=<strong-random-key>
    export ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
"""

import os
from .settings import *  # noqa: F401, F403

# ---------------------------------------------------------------------------
# Core security
# ---------------------------------------------------------------------------
DEBUG = False

# Required in production — no insecure default
SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

# ---------------------------------------------------------------------------
# HTTPS hardening (uncomment when behind TLS terminator / reverse proxy)
# ---------------------------------------------------------------------------
# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True
# SECURE_SSL_REDIRECT = True
# SECURE_HSTS_SECONDS = 31536000
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# ---------------------------------------------------------------------------
# Remove dev-only apps
# ---------------------------------------------------------------------------
INSTALLED_APPS = [app for app in INSTALLED_APPS if app != "django_browser_reload"]

# ---------------------------------------------------------------------------
# WhiteNoise — serve compressed static files from memory (no nginx needed)
# Insert immediately after SecurityMiddleware (index 0)
# ---------------------------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
] + [m for m in MIDDLEWARE if m != "django.middleware.security.SecurityMiddleware"]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
WHITENOISE_MANIFEST_STRICT = False  # survive collectstatic cache misses gracefully

# ---------------------------------------------------------------------------
# Database
# Provide DB_ENGINE + DB_NAME (+ optional DB_USER / DB_PASSWORD / DB_HOST /
# DB_PORT) to use Oracle or Postgres.  Omit to run in SQLite / Demo Mode.
# ---------------------------------------------------------------------------
_db_engine = os.environ.get("DB_ENGINE", "")
if _db_engine:
    DATABASES = {
        "default": {
            "ENGINE": _db_engine,
            "NAME": os.environ["DB_NAME"],
            "USER": os.environ.get("DB_USER", ""),
            "PASSWORD": os.environ.get("DB_PASSWORD", ""),
            "HOST": os.environ.get("DB_HOST", ""),
            "PORT": os.environ.get("DB_PORT", ""),
        }
    }
else:
    # Demo / SQLite fallback — no external DB required
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",  # noqa: F405
        }
    }

# ---------------------------------------------------------------------------
# Oracle RMAN Catalog — read from env; None activates DemoRmanRepository
# ---------------------------------------------------------------------------
_oracle_user = os.environ.get("ORACLE_CATALOG_USER", "")
if _oracle_user:
    ORACLE_CATALOG = {
        "user": _oracle_user,
        "password": os.environ.get("ORACLE_CATALOG_PASSWORD", ""),
        "dsn": os.environ.get("ORACLE_CATALOG_DSN", ""),
    }
else:
    ORACLE_CATALOG = None  # Demo mode

# Demo Mode flag (mirrored from settings_local for view logic compatibility)
DEMO_MODE = not bool(_oracle_user)

# ---------------------------------------------------------------------------
# SLA Alerting — webhook URL for check_backup_sla command (optional)
# When set, breaches are POSTed as JSON; otherwise StubNotificationGateway logs only.
# ---------------------------------------------------------------------------
SLA_ALERT_WEBHOOK_URL = os.environ.get("SLA_ALERT_WEBHOOK_URL", "").strip() or None

# ---------------------------------------------------------------------------
# Structured container logging — everything to stdout, WARNING+ globally,
# INFO+ for relback namespace.
# ---------------------------------------------------------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "%(asctime)s %(levelname)s %(name)s %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    },
    "root": {"handlers": ["console"], "level": "WARNING"},
    "loggers": {
        "relback": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "django.request": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
        },
    },
}
