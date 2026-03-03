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
        ru = RelbackUser(username="logintest", status=1, email="login@test.com")
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
        self.assertTrue(RelbackUser.objects.filter(username="newuser").exists())
