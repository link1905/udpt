from account.test import LiveServerAuthenticatedTestCase
from django.urls import reverse
from forum.models import TaggedThread, Thread
from taggit.models import Tag


class TestThreadVoteAPI(LiveServerAuthenticatedTestCase):
    def setUp(self) -> None:
        super().setUp()

        self.question = Thread.objects.create(
            title="testthread",
            content="test",
            creator_id=self.user.id,
            creator_name=self.user.get_full_name(),
            creator_email=self.user.email,
        )
        self.approved_question = Thread.objects.create(
            title="testthread staff",
            content="test",
            creator_id=self.user.id,
            creator_name=self.user.get_full_name(),
            creator_email=self.user.email,
            approved=True,
            approver_id=self.staff.id,
            approver_name=self.staff.get_full_name(),
            approver_email=self.staff.email,
        )

        self.tag1 = Tag.objects.create(name="tag1")
        self.tag2 = Tag.objects.create(name="tag2")

        self.tagged_thread1 = TaggedThread.objects.create(
            thread=self.question,
            tag_id=self.tag1.pk,
        )
        self.tagged_thread2 = TaggedThread.objects.create(
            thread=self.question,
            tag_id=self.tag2.pk,
        )
        self.approved_tagged_thread = TaggedThread.objects.create(
            thread=self.approved_question,
            tag_id=self.tag1.pk,
        )

    def test_list(self):
        url = reverse("tagged-thread-list-create")

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["results"]), 1)

        response = self.user_client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["results"]), 3)

        response = self.staff_client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["results"]), 3)

    def test_detail(self):
        url = reverse("tagged-thread-detail-delete", args=(self.tagged_thread1.pk,))
        url2 = reverse(
            "tagged-thread-detail-delete", args=(self.approved_tagged_thread.pk,)
        )

        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

        response = self.client.get(url2)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["pk"], self.approved_tagged_thread.pk)

        response = self.user_client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["pk"], self.tagged_thread1.pk)

        response = self.staff_client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["pk"], self.tagged_thread1.pk)

    def test_create(self):
        url = reverse("tagged-thread-list-create")

        response = self.client.post(
            url,
            data={
                "thread": self.approved_question.pk,
                "tag_id": self.tag2.pk,
            },
        )
        self.assertEqual(response.status_code, 403)

        response = self.user_client.post(
            url,
            data={
                "thread": self.approved_question.pk,
                "tag_id": self.tag2.pk,
            },
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["fields"]["thread"], self.approved_question.pk)
        self.assertEqual(response.json()["fields"]["tag_id"], self.tag2.pk)

        response = self.user_client.post(
            url,
            data={
                "thread": self.approved_question.pk,
                "tag_id": 2001,
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_delete(self):
        url = reverse("tagged-thread-detail-delete", args=(self.tagged_thread1.pk,))
        url2 = reverse("tagged-thread-detail-delete", args=(self.tagged_thread2.pk,))

        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)

        response = self.user_client.delete(url)
        self.assertEqual(response.status_code, 204)

        response = self.staff_client.delete(url2)
        self.assertEqual(response.status_code, 204)

    def test_filter_tag_id(self):
        url = reverse("tagged-thread-list-create")

        response = self.staff_client.get(
            url,
            data={
                "tag_id": self.tag1.pk,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["results"]), 2)

    def test_filter_thread(self):
        url = reverse("tagged-thread-list-create")

        response = self.staff_client.get(
            url,
            data={
                "thread": self.question.pk,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["results"]), 2)
