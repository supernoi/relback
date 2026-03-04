"""
Oracle RMAN Catalog connection helper.

Provides a Dependency Inversion wrapper over python-oracledb.
Returns None gracefully when ORACLE_CATALOG is not configured in settings,
or when the catalog host is unreachable.

Multi-tenant (Phase 19): when client_id is set and that Client has catalog_dsn,
uses that DSN with global credentials; otherwise uses global ORACLE_CATALOG.

Usage (inside a repository):
    from coreRelback.gateways.oracle_catalog import get_catalog_connection
    conn = get_catalog_connection(client_id=request_client_id)
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


def get_catalog_connection(client_id: Optional[int] = None) -> Optional[oracledb.Connection]:
    """Return a thin-mode oracledb connection to the RMAN Recovery Catalog.

    When client_id is given and that Client has catalog_dsn set, uses that DSN
    with global ORACLE_CATALOG user/password. Otherwise uses global config.

    Returns None when:
    - ``ORACLE_CATALOG`` is not set in Django settings (e.g. dev / CI)
    - The catalog host is unreachable (network timeout, wrong credentials, etc.)

    Never raises — callers always receive a valid connection or ``None``.
    """
    config: Optional[dict] = getattr(settings, "ORACLE_CATALOG", None)
    if not config:
        logger.debug(
            "ORACLE_CATALOG not configured — skipping catalog query."
        )
        return None

    dsn = config["dsn"]
    if client_id is not None:
        try:
            from coreRelback.models import Client
            client = Client.objects.filter(pk=client_id).first()
            if client and getattr(client, "catalog_dsn", None):
                dsn = client.catalog_dsn.strip()
        except Exception as exc:
            logger.debug("Resolving client catalog_dsn failed: %s — using global.", exc)

    try:
        conn = oracledb.connect(
            user=config["user"],
            password=config["password"],
            dsn=dsn,
        )
        return conn
    except Exception as exc:  # pragma: no cover — requires live Oracle
        logger.warning(
            "Oracle RMAN Catalog unavailable (%s: %s) — returning empty results.",
            type(exc).__name__,
            exc,
        )
        return None
