"""
Oracle RMAN Catalog connection helper.

Provides a Dependency Inversion wrapper over python-oracledb.
Returns None gracefully when ORACLE_CATALOG is not configured in settings,
or when the catalog host is unreachable.

Usage (inside a repository):
    from coreRelback.gateways.oracle_catalog import get_catalog_connection
    conn = get_catalog_connection()
    if conn is None:
        return []          # graceful fallback
    with conn:
        cursor = conn.cursor()
        ...
"""
import logging
from typing import Optional

import oracledb
from django.conf import settings

logger = logging.getLogger(__name__)


def get_catalog_connection() -> Optional[oracledb.Connection]:
    """Return a thin-mode oracledb connection to the RMAN Recovery Catalog.

    Returns None when:
    - ``ORACLE_CATALOG`` is not set in Django settings (e.g. dev / CI)
    - The catalog host is unreachable (network timeout, wrong credentials, etc.)

    Never raises — callers always receive a valid connection or ``None``.
    The ``with conn:`` context manager commits/closes automatically.
    """
    config: Optional[dict] = getattr(settings, "ORACLE_CATALOG", None)
    if not config:
        logger.debug(
            "ORACLE_CATALOG not configured — skipping catalog query."
        )
        return None

    try:
        conn = oracledb.connect(
            user=config["user"],
            password=config["password"],
            dsn=config["dsn"],
        )
        return conn
    except Exception as exc:  # pragma: no cover — requires live Oracle
        logger.warning(
            "Oracle RMAN Catalog unavailable (%s: %s) — returning empty results.",
            type(exc).__name__,
            exc,
        )
        return None
