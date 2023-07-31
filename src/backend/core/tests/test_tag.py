from account.test import AuthenticatedTestCase
from django.urls import reverse
from forum.models import Thread
from taggit.models import Tag


class TestTagAPI(AuthenticatedTestCase):
    databases = ["account", "forum", "tag"]

    def test_list(self):
        url = reverse("tag-list")

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

    def test_filter_search(self):
        Tag.objects.create(name="testtag1")
        Tag.objects.create(name="testtag2")
        Tag.objects.create(name="testtag3")

        url = reverse("tag-list")

        response = self.client.get(url, {"search": "testtag2"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["results"]), 1)
        self.assertEqual(response.json()["results"][0]["fields"]["name"], "testtag2")

    def test_filter_thread(self):
        thread = Thread.objects.create(
            title="testthread", content="test", creator=self.user
        )
        thread_2 = Thread.objects.create(
            title="testthread", content="test", creator=self.user
        )

        thread.tags.add("testtag1")
        thread_2.tags.add("testtag2")

        url = reverse("tag-list")

        response = self.client.get(url, {"thread": thread.pk})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["results"]), 1)
        self.assertEqual(response.json()["results"][0]["fields"]["name"], "testtag1")
