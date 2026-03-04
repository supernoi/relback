"""
Tests for REST API (Phase 17).
"""
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse


class BackupAuditAPITests(TestCase):
    """GET /api/backup-audit/ requires auth and returns JSON with jobs + summary."""

    def test_unauthenticated_returns_403(self):
        """DRF IsAuthenticated returns 403 Forbidden when not logged in."""
        response = self.client.get(reverse("api:backup-audit-list"))
        self.assertEqual(response.status_code, 403)

    def test_authenticated_returns_200_with_jobs_and_summary(self):
        user = User.objects.create_user(
            username="apitest", password="testpass123", is_active=True
        )
        self.client.force_login(user)
        response = self.client.get(reverse("api:backup-audit-list"))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("jobs", data)
        self.assertIn("summary", data)
        self.assertIsInstance(data["jobs"], list)
        summary = data["summary"]
        self.assertIn("total", summary)
        self.assertIn("successful", summary)
        self.assertIn("failed", summary)
        self.assertIn("running", summary)
        self.assertIn("oracle_available", summary)
