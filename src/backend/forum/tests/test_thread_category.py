from account.test import LiveServerAuthenticatedTestCase
from django.urls import reverse
from forum.models import ThreadCategory


class TestThreadCategoryAPI(LiveServerAuthenticatedTestCase):
    def setUp(self) -> None:
        super().setUp()
        
        self.category = ThreadCategory.objects.create(name="testcategory")
        self.category2 = ThreadCategory.objects.create(name="testcategory2")


    def test_list(self):
        url = reverse("thread-category-list-create")

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["results"]), 2)
        self.assertEqual(response.json()["count"], 2)

        response = self.user_client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["results"]), 2)
        self.assertEqual(response.json()["count"], 2)

        response = self.staff_client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["results"]), 2)
        self.assertEqual(response.json()["count"], 2)

    def test_detail(self):
        url = reverse("thread-category-detail-update-delete", kwargs={"pk": self.category.pk})

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["pk"], self.category.pk)

        response = self.user_client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["pk"], self.category.pk)

        response = self.staff_client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["pk"], self.category.pk)

    def test_create(self):
        url = reverse("thread-category-list-create")

        response = self.client.post(url, data={"name": "test"})
        self.assertEqual(response.status_code, 403)

        response = self.user_client.post(url, data={"name": "test"})
        self.assertEqual(response.status_code, 403)

        response = self.staff_client.post(url, data={"name": "testcategory"})
        self.assertEqual(response.status_code, 400)

        response = self.staff_client.post(url, data={"name": "test"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["fields"]["name"], "test")

    def test_update(self):
        url = reverse("thread-category-detail-update-delete", kwargs={"pk": self.category.pk})

        response = self.client.put(url, data={"name": "test"}, content_type="application/json")
        self.assertEqual(response.status_code, 403)

        response = self.user_client.put(url, data={"name": "test"}, content_type="application/json")
        self.assertEqual(response.status_code, 403)

        response = self.staff_client.put(url, data={"name": "test"}, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["fields"]["name"], "test")

    def test_delete(self):
        url = reverse("thread-category-detail-update-delete", kwargs={"pk": self.category.pk})

        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)

        response = self.user_client.delete(url)
        self.assertEqual(response.status_code, 403)

        response = self.staff_client.delete(url)
        self.assertEqual(response.status_code, 204)

    def test_filter_search(self):
        url = reverse("thread-category-list-create")

        response = self.client.get(url, data={"search": "2"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["results"]), 1)
        self.assertEqual(response.json()["count"], 1)

