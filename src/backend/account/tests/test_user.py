from account.test import AuthenticatedTestCase
from django.test.client import MULTIPART_CONTENT
from django.urls import reverse


class TestUserAPI(AuthenticatedTestCase):
    def test_list(self):
        url = reverse("user-list-create")

        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        response = self.user_client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["results"]), 1)
        self.assertEqual(response.json()["results"][0]["pk"], self.user.pk)

        response = self.staff_client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["results"]), 2)
        self.assertEqual(response.json()["results"][0]["pk"], self.user.pk)
        self.assertEqual(response.json()["results"][1]["pk"], self.staff.pk)

    def test_create_user(self):
        url = reverse("user-list-create")

        response = self.client.post(
            url,
            {
                "username": "testuser2",
                "password1": "TestPass123123",
                "password2": "TestPass123123",
                "is_active": True,
            },
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["fields"]["username"], "testuser2")
        self.assertEqual(response.json()["fields"]["is_active"], True)

    def test_detail_user(self):
        url = reverse("user-detail-update-delete", kwargs={"pk": self.user.pk})

        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        response = self.user_client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["pk"], self.user.pk)

        response = self.staff_client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["pk"], self.user.pk)

    def test_update_user(self):
        url = reverse("user-detail-update-delete", kwargs={"pk": self.user.pk})

        response = self.client.put(url, {"username": "testuser2"})
        self.assertEqual(response.status_code, 403)

        data = self.user_client._encode_data(
            {"username": "testuser2"}, MULTIPART_CONTENT
        )
        response = self.user_client.put(url, data, content_type=MULTIPART_CONTENT)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["pk"], self.user.pk)
        self.assertEqual(response.json()["fields"]["username"], "testuser2")

        data = self.staff_client._encode_data(
            {"username": "testuser3", "date_joined": "2021-01-01T00:00:00Z"},
            MULTIPART_CONTENT,
        )
        response = self.staff_client.put(url, data, content_type=MULTIPART_CONTENT)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["pk"], self.user.pk)
        self.assertEqual(response.json()["fields"]["username"], "testuser3")

    def test_delete_user(self):
        url = reverse("user-detail-update-delete", kwargs={"pk": self.user.pk})

        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)

        response = self.user_client.delete(url)
        self.assertEqual(response.status_code, 204)
