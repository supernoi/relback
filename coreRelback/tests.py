"""
Integration tests for coreRelback views.

Two test classes cover different concerns:
  - AuthRedirectTests (SimpleTestCase): no DB required. Verifies that every
    protected URL returns 302 to /login/ for unauthenticated requests.
  - AuthenticatedTemplateTests (TestCase): requires SQLite test DB.
    Verifies that authenticated requests render the expected templates.

Run with:
    DJANGO_SETTINGS_MODULE=projectRelback.settings_test \\
        python manage.py test coreRelback.tests --verbosity=2
"""
from django.contrib.auth import get_user_model
from django.test import SimpleTestCase, TestCase
from django.urls import reverse

User = get_user_model()


class AuthRedirectTests(SimpleTestCase):
    """Unauthenticated GET requests must be redirected to the login page.

    Uses SimpleTestCase so no database is required — this class can also
    run under settings_dev (DATABASES = {}).
    """

    def _assert_login_redirect(self, url: str) -> None:
        response = self.client.get(url)
        self.assertEqual(
            response.status_code, 302,
            msg=f"Expected 302 for unauthenticated GET {url}, got {response.status_code}",
        )
        self.assertIn(
            "/login/", response["Location"],
            msg=f"Redirect for {url} should point to /login/",
        )

    def test_index_redirects_unauthenticated(self):
        self._assert_login_redirect(reverse("coreRelback:index"))

    def test_client_list_redirects_unauthenticated(self):
        self._assert_login_redirect(reverse("coreRelback:client-list"))

    def test_host_list_redirects_unauthenticated(self):
        self._assert_login_redirect(reverse("coreRelback:host-list"))

    def test_database_list_redirects_unauthenticated(self):
        self._assert_login_redirect(reverse("coreRelback:database-list"))

    def test_policy_list_redirects_unauthenticated(self):
        self._assert_login_redirect(reverse("coreRelback:policy-list"))

    def test_report_read_redirects_unauthenticated(self):
        self._assert_login_redirect(reverse("coreRelback:report-read"))

    def test_user_settings_redirects_unauthenticated(self):
        self._assert_login_redirect(reverse("coreRelback:user-settings"))

    def test_creators_is_public(self):
        """creators() is intentionally public — no auth required."""
        response = self.client.get(reverse("coreRelback:creators"))
        self.assertEqual(response.status_code, 200)


class AuthenticatedTemplateTests(TestCase):
    """Authenticated GET requests must render the expected templates.

    Requires the SQLite test database (settings_test.py).
    A superuser is created in setUp() and force_login'd before each test so
    no RelbackUser profile is needed for read-only list/index views.
    """

    def setUp(self):
        self.user = User.objects.create_superuser(
            username="testadmin",
            password="testpass123",
            email="testadmin@example.com",
        )
        self.client.force_login(self.user)

    def test_index_template(self):
        response = self.client.get(reverse("coreRelback:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")

    def test_client_list_template(self):
        response = self.client.get(reverse("coreRelback:client-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "clients.html")

    def test_host_list_template(self):
        response = self.client.get(reverse("coreRelback:host-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "hosts.html")

    def test_database_list_template(self):
        response = self.client.get(reverse("coreRelback:database-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "databases.html")

    def test_policy_list_template(self):
        response = self.client.get(reverse("coreRelback:policy-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "policies.html")

    def test_report_read_template(self):
        response = self.client.get(reverse("coreRelback:report-read"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "reports.html")

    def test_report_read_context_keys_present(self):
        """report_read must supply all context keys consumed by reports.html."""
        response = self.client.get(reverse("coreRelback:report-read"))
        self.assertEqual(response.status_code, 200)
        for key in ("jobs", "oracle_available", "successful_jobs",
                    "failed_jobs", "today_jobs", "running_jobs"):
            self.assertIn(key, response.context,
                          f"'{key}' missing from report_read context")

    def test_report_read_oracle_unavailable_in_test_env(self):
        """In the test environment ORACLE_CATALOG=None so oracle_available must be False."""
        response = self.client.get(reverse("coreRelback:report-read"))
        self.assertIs(response.context["oracle_available"], False)
        self.assertIsInstance(response.context["jobs"], list)
        self.assertEqual(response.context["running_jobs"], 0)

    def test_creators_template_public(self):
        """creators() renders even for unauthenticated users."""
        self.client.logout()
        response = self.client.get(reverse("coreRelback:creators"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "creators.html")


class LoginViewTests(TestCase):
    """Tests for the /login/ endpoint wired to Django's built-in LoginView."""

    def setUp(self):
        from coreRelback.models import RelbackUser
        ru = RelbackUser(username="logintest", status=1,
                         email="login@test.com")
        ru.set_password("pass1234!")
        ru.save()

    def test_login_page_renders(self):
        response = self.client.get(reverse("coreRelback:login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth/login.html")

    def test_valid_credentials_redirect_to_home(self):
        response = self.client.post(
            reverse("coreRelback:login"),
            {"username": "logintest", "password": "pass1234!"},
        )
        # Should redirect to LOGIN_REDIRECT_URL = '/'
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "/")

    def test_invalid_credentials_show_form_again(self):
        response = self.client.post(
            reverse("coreRelback:login"),
            {"username": "logintest", "password": "wrongpassword"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth/login.html")


class LogoutRegisterTests(TestCase):
    """Tests for logout and register endpoints."""

    def setUp(self):
        self.django_user = User.objects.create_user(
            username="logouttest", password="pass1234!"
        )

    def test_logout_redirects_to_login(self):
        self.client.force_login(self.django_user)
        response = self.client.post(reverse("coreRelback:logout"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response["Location"])

    def test_register_page_renders(self):
        response = self.client.get(reverse("coreRelback:register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth/register.html")

    def test_register_creates_account_and_redirects(self):
        response = self.client.post(
            reverse("coreRelback:register"),
            {
                "username": "newuser",
                "name": "New User",
                "email": "new@test.com",
                "password1": "securepass99!",
                "password2": "securepass99!",
            },
        )
        from coreRelback.models import RelbackUser
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response["Location"])
        self.assertTrue(RelbackUser.objects.filter(
            username="newuser").exists())


class BackupBadgeTagTests(SimpleTestCase):
    """Unit tests for the backup_badge template tag presenter.

    These run without a database (SimpleTestCase) since the tag is purely
    presentational and has no DB interaction.
    """

    def _render(self, status_str: str, compact: bool = False) -> str:
        from coreRelback.templatetags.backup_tags import backup_badge
        return backup_badge(status_str, compact=compact)

    def test_completed_renders_success_badge(self):
        html = self._render("COMPLETED")
        self.assertIn("badge-success", html)
        self.assertIn("check_circle", html)
        self.assertIn("Completed", html)

    def test_failed_renders_error_badge(self):
        html = self._render("FAILED")
        self.assertIn("badge-error", html)
        self.assertIn("error_outline", html)
        self.assertIn("Failed", html)

    def test_running_renders_info_badge(self):
        html = self._render("RUNNING")
        self.assertIn("badge-info", html)
        self.assertIn("sync", html)

    def test_warning_renders_warning_badge(self):
        html = self._render("WARNING")
        self.assertIn("badge-warning", html)
        self.assertIn("warning", html)

    def test_interrupted_renders_violet_ghost_badge(self):
        html = self._render("INTERRUPTED")
        self.assertIn("badge-ghost", html)
        self.assertIn("#a78bfa", html)  # violet token from tailwind.config.js
        self.assertIn("block", html)    # Material icon name
        self.assertIn("Interrupted", html)

    def test_unknown_renders_neutral_badge(self):
        html = self._render("UNKNOWN")
        self.assertIn("badge-neutral", html)

    def test_unknown_key_falls_back_to_neutral(self):
        html = self._render("SOME_FUTURE_STATUS")
        self.assertIn("badge-neutral", html)

    def test_compact_hides_label_shows_title(self):
        html = self._render("COMPLETED", compact=True)
        self.assertIn("badge-sm", html)
        self.assertIn('title="Completed"', html)
        self.assertNotIn(">Completed<", html)

    def test_accepts_enum_member(self):
        from coreRelback.domain.entities import BackupStatusValue
        html = self._render(BackupStatusValue.FAILED)
        self.assertIn("badge-error", html)


# ---------------------------------------------------------------------------
# Report Log Detail View Integration Tests
# ---------------------------------------------------------------------------

class ReportLogDetailViewTests(TestCase):
    """Integration tests for the report_read_log_detail view.

    No real Oracle catalog required — settings_test.py sets ORACLE_CATALOG=None.
    The view must render gracefully with an empty log and no exec detail.
    """

    def setUp(self):
        from django.contrib.auth.models import User
        self.user = User.objects.create_superuser(
            username="logdetail_admin",
            password="testpass123",
            email="logdetail@example.com",
        )
        self.client.force_login(self.user)

    def _url(self, policy_id=999, db_key=1, session_key=1):
        return reverse(
            "coreRelback:report-read-log-detail",
            kwargs={"idPolicy": policy_id, "dbKey": db_key,
                    "sessionKey": session_key},
        )

    def test_log_detail_redirects_unauthenticated(self):
        """Unauthenticated users must be redirected to login."""
        self.client.logout()
        response = self.client.get(self._url())
        self.assertIn(response.status_code, (302, 301))
        self.assertIn("/login/", response["Location"])

    def test_log_detail_renders_template(self):
        """Authenticated GET must render reportsReadLog.html with 200."""
        response = self.client.get(self._url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "reportsReadLog.html")

    def test_log_detail_context_keys_present(self):
        """View must supply all context keys consumed by the template."""
        response = self.client.get(self._url())
        self.assertEqual(response.status_code, 200)
        for key in ("policyDetail", "execDetail", "reportLog", "oracle_available",
                    "idPolicy", "dbKey", "sessionKey"):
            self.assertIn(key, response.context,
                          f"'{key}' missing from report_read_log_detail context")

    def test_log_detail_oracle_unavailable_in_test_env(self):
        """Oracle catalog is None in test env — execDetail=None, reportLog=[], oracle_available=False."""
        response = self.client.get(self._url())
        self.assertIs(response.context["oracle_available"], False)
        self.assertIsNone(response.context["execDetail"])
        self.assertEqual(response.context["reportLog"], [])

    def test_log_detail_policy_not_found_no_500(self):
        """When idPolicy doesn't exist in SQLite, policyDetail=None and view returns 200."""
        response = self.client.get(self._url(policy_id=99999))
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.context["policyDetail"])
