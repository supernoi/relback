"""
Optional integration tests for Oracle RMAN Catalog gateway.

Run only when ORACLE_CATALOG_* env vars are set (e.g. local or staging).
Skipped in CI when catalog is not available — no Oracle required for main test suite.

Run explicitly:
  ORACLE_CATALOG_USER=... ORACLE_CATALOG_PASSWORD=... ORACLE_CATALOG_DSN=... \\
  python manage.py test coreRelback.tests_oracle_integration
"""
import os
import unittest

from django.test import TestCase, override_settings

from coreRelback.gateways.repositories import OracleRmanRepository


def _oracle_catalog_from_env():
    """Build ORACLE_CATALOG dict from env if all required vars are set."""
    user = os.environ.get("ORACLE_CATALOG_USER", "")
    dsn = os.environ.get("ORACLE_CATALOG_DSN", "")
    if not user or not dsn:
        return None
    return {
        "user": user,
        "password": os.environ.get("ORACLE_CATALOG_PASSWORD", ""),
        "dsn": dsn,
    }


@unittest.skipUnless(
    _oracle_catalog_from_env(),
    "ORACLE_CATALOG_USER and ORACLE_CATALOG_DSN must be set to run Oracle integration tests",
)
class OracleRmanRepositoryIntegrationTest(TestCase):
    """
    Live-catalog tests: ensure OracleRmanRepository returns list without crashing.

    Skipped when ORACLE_CATALOG_* is not set (CI / demo-only environments).
    """

    @override_settings(ORACLE_CATALOG=_oracle_catalog_from_env())
    def test_get_backup_jobs_returns_list(self):
        """get_backup_jobs() returns a list (empty or with items); no exception."""
        repo = OracleRmanRepository()
        result = repo.get_backup_jobs()
        self.assertIsInstance(result, list)
