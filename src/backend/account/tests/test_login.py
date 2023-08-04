from django.contrib.auth import get_user_model
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

User = get_user_model()


class TestLogin(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login(self):
        User.objects.create_user(
            username="testuser", password="testpass", is_active=True
        )
        url = reverse("login")

        response = self.client.post(
            url, {"username": "testuser", "password": "testpass"}
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn("token", response.json())
        self.assertIn("user", response.json())
        self.assertEqual(response.json()["user"]["fields"]["username"], "testuser")
        self.assertEqual(response.json()["user"]["fields"]["is_active"], True)

        token = response.json()["token"]
        refresh_url = reverse("auth-refresh")

        response = self.client.post(refresh_url, HTTP_AUTHORIZATION=f"Bearer {token}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.json())
        self.assertIn("user", response.json())
        self.assertEqual(response.json()["user"]["fields"]["username"], "testuser")
        self.assertEqual(response.json()["user"]["fields"]["is_active"], True)

    def test_password_change(self):
        user = User.objects.create_user(
            username="testuser", password="testpass", is_active=True
        )
        url = reverse("login")

        response = self.client.post(
            url, {"username": "testuser", "password": "testpass"}
        )
        self.assertEqual(response.status_code, 201)

        token = response.json()["token"]
        change_password_url = reverse("change-password")

        response = self.client.post(
            change_password_url,
            {
                "old_password": "testpass",
                "new_password1": "newtestpass",
                "new_password2": "newtestpass",
            },
            HTTP_AUTHORIZATION=f"Bearer {token}",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["pk"], user.pk)

        response = self.client.post(
            url, {"username": "testuser", "password": "newtestpass"}
        )
        self.assertEqual(response.status_code, 201)
