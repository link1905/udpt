from account.test import LiveServerAuthenticatedTestCase
from django.urls import reverse
from taggit.models import Tag


class TestTagAPI(LiveServerAuthenticatedTestCase):
    def test_list(self):
        url = reverse("tag-list-create")

        Tag.objects.create(name="testtag1")

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["results"]), 1)
        self.assertEqual(response.json()["count"], 1)

    def test_detail(self):
        tag = Tag.objects.create(name="testtag1")
        url = reverse("tag-detail", kwargs={"pk": tag.pk})

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["pk"], tag.pk)
        self.assertEqual(response.json()["fields"]["name"], "testtag1")

    def test_create(self):
        url = reverse("tag-list-create")

        response = self.client.post(url, {"name": "testtag1"})
        self.assertEqual(response.status_code, 403)

        response = self.user_client.post(url, {"name": "testtag1"})
        print(response.json())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["fields"]["name"], "testtag1")

    def test_filter_search(self):
        Tag.objects.create(name="testtag1")
        Tag.objects.create(name="testtag2")
        Tag.objects.create(name="testtag3")

        url = reverse("tag-list-create")

        response = self.client.get(url, {"search": "testtag2"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["results"]), 1)
        self.assertEqual(response.json()["results"][0]["fields"]["name"], "testtag2")
