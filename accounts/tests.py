from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core import mail
from accounts.models import Profile


class AccountsViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="hossein_r",
            email="hossein@example.com",
            first_name="حسین",
            last_name="رحمتی",
            password="SecurePassword123!",
        )

    def test_login_view_get(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/login.html")

    def test_login_with_username_success(self):
        response = self.client.post(
            reverse("login"),
            {"username": "hossein_r", "password": "SecurePassword123!", "remember_me": True},
            follow=True,
        )
        self.assertTrue(response.context["user"].is_authenticated)
        self.assertRedirects(response, reverse("dashboard"))

    def test_login_with_email_success(self):
        response = self.client.post(
            reverse("login"),
            {"username": "HOSSEIN@EXAMPLE.COM", "password": "SecurePassword123!", "remember_me": True},
            follow=True,
        )
        self.assertTrue(response.context["user"].is_authenticated)
        self.assertRedirects(response, reverse("dashboard"))

    def test_login_invalid_credentials(self):
        response = self.client.post(
            reverse("login"),
            {"username": "hossein_r", "password": "WrongPassword!"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["user"].is_authenticated)
        self.assertFormError(response.context["form"], None, "نام کاربری (یا ایمیل) یا رمز عبور اشتباه است.")

    def test_register_view_get(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/register.html")

    def test_register_view_post_success(self):
        response = self.client.post(
            reverse("register"),
            {
                "first_name": "سارا",
                "last_name": "احمدی",
                "username": "sara_ahmadi",
                "email": "sara@example.com",
                "password1": "StrongPass2026!",
                "password2": "StrongPass2026!",
            },
            follow=True,
        )
        self.assertRedirects(response, reverse("dashboard"))
        new_user = User.objects.get(username="sara_ahmadi")
        self.assertEqual(new_user.email, "sara@example.com")
        self.assertTrue(Profile.objects.filter(user=new_user).exists())
        self.assertTrue(response.context["user"].is_authenticated)

    def test_register_duplicate_email_fails(self):
        response = self.client.post(
            reverse("register"),
            {
                "first_name": "تست",
                "last_name": "تستی",
                "username": "unique_username",
                "email": "HOSSEIN@EXAMPLE.COM",
                "password1": "StrongPass2026!",
                "password2": "StrongPass2026!",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context["form"], "email", "کاربری با این ایمیل قبلاً ثبت‌نام کرده است.")

    def test_logout_view(self):
        self.client.login(username="hossein_r", password="SecurePassword123!")
        response = self.client.post(reverse("logout"), follow=True)
        self.assertFalse(response.context["user"].is_authenticated)
        self.assertRedirects(response, reverse("core:home"))

    def test_dashboard_view_unauthenticated_redirect(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 302)

    def test_dashboard_view_authenticated(self):
        self.client.login(username="hossein_r", password="SecurePassword123!")
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboard/dashboard.html")

    def test_profile_settings_view_get(self):
        self.client.login(username="hossein_r", password="SecurePassword123!")
        response = self.client.get(reverse("profile_settings"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/profile_settings.html")

    def test_profile_settings_view_update(self):
        self.client.login(username="hossein_r", password="SecurePassword123!")
        response = self.client.post(
            reverse("profile_settings"),
            {
                "first_name": "حسین",
                "last_name": "رحمتی نژاد",
                "email": "hossein_new@example.com",
                "headline": "Senior Full-Stack Developer",
                "phone_number": "09123456789",
                "bio": "علاقه‌مند به هوش مصنوعی و توسعه نرم‌افزار",
            },
            follow=True,
        )
        self.assertRedirects(response, reverse("profile_settings"))
        self.user.refresh_from_db()
        self.assertEqual(self.user.last_name, "رحمتی نژاد")
        self.assertEqual(self.user.email, "hossein_new@example.com")
        self.assertEqual(self.user.profile.headline, "Senior Full-Stack Developer")
        self.assertEqual(self.user.profile.phone_number, "09123456789")

    def test_password_reset_flow(self):
        response = self.client.post(
            reverse("password_reset"),
            {"email": "hossein@example.com"},
            follow=True,
        )
        self.assertRedirects(response, reverse("password_reset_done"))
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("بازیابی رمز عبور", mail.outbox[0].subject)


