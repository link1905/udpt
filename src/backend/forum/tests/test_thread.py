from account.test import AuthenticatedTestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import ContentType
from django.urls import reverse
from django.utils import timezone
from forum.models import Thread, ThreadVote

User = get_user_model()


class TestThreadAPI(AuthenticatedTestCase):
    databases = ["account", "forum", "tag"]

    def setUp(self) -> None:
        super().setUp()

        self.user_type = ContentType.objects.get_for_model(User)

        self.question = Thread.objects.create(
            title="testthread", content="test", creator=self.user
        )
        self.question.tags.add("test", "test2")
        self.answer = Thread.objects.create(
            title="testthread", content="test", creator=self.user, parent=self.question
        )
        Thread.objects.create(
            title="testthread", content="test", creator=self.user, parent=self.answer
        )

        self.created_start = timezone.now()
        self.approved_question = Thread.objects.create(
            title="testthread staff",
            content="test",
            creator=self.user,
            approved=True,
            approver=self.staff,
            approver_name=self.staff.get_full_name(),
            approver_email=self.staff.email,
        )
        self.approved_question.tags.add("test3", "test4")
        self.created_end = timezone.now()
        self.approved_answer = Thread.objects.create(
            title="testthread staff",
            content="test",
            creator=self.user,
            parent=self.approved_question,
            approved=True,
            approver=self.staff,
            approver_name=self.staff.get_full_name(),
            approver_email=self.staff.email,
        )
        Thread.objects.create(
            title="testthread staff",
            content="test",
            creator=self.user,
            parent=self.approved_answer,
        )

    def test_list(self):
        url = reverse("thread-list-create")

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["results"]), 3)
        self.assertEqual(response.json()["count"], 3)

        response = self.user_client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["results"]), 6)
        self.assertEqual(response.json()["count"], 6)

        response = self.staff_client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["results"]), 6)
        self.assertEqual(response.json()["count"], 6)

    def test_detail(self):
        url = reverse("thread-detail-update-delete", kwargs={"pk": self.question.pk})
        url2 = reverse(
            "thread-detail-update-delete", kwargs={"pk": self.approved_question.pk}
        )

        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

        response = self.client.get(url2)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["pk"], self.approved_question.pk)

        response = self.user_client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["pk"], self.question.pk)

        response = self.staff_client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["pk"], self.question.pk)

    def test_create(self):
        url = reverse("thread-list-create")

        response = self.client.post(
            url,
            {
                "title": "testthread",
                "content": "test",
                "parent": self.approved_question.pk,
            },
        )
        self.assertEqual(response.status_code, 403)

        response = self.user_client.post(
            url,
            {
                "title": "testthread",
                "content": "test",
                "parent": self.question.pk,
            },
        )
        self.assertEqual(response.status_code, 400)

        response = self.user_client.post(
            url,
            {
                "title": "testthread",
                "content": "test",
                "parent": self.approved_question.pk,
            },
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["fields"]["title"], "testthread")
        self.assertEqual(response.json()["fields"]["content"], "test")
        self.assertEqual(response.json()["fields"]["parent"], self.approved_question.pk)
        self.assertEqual(response.json()["fields"]["creator_id"], self.user.pk)
        self.assertEqual(response.json()["fields"]["creator_type"], self.user_type.pk)
        self.assertEqual(response.json()["fields"]["approver_type"], None)
        self.assertEqual(response.json()["fields"]["approver_id"], None)
        self.assertEqual(response.json()["fields"]["approved"], False)
        self.assertEqual(response.json()["fields"]["approver_name"], "")
        self.assertEqual(response.json()["fields"]["approver_email"], "")

        response = self.staff_client.post(
            url,
            {
                "title": "testthread",
                "content": "test",
                "parent": self.approved_question.pk,
            },
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["fields"]["title"], "testthread")
        self.assertEqual(response.json()["fields"]["content"], "test")
        self.assertEqual(response.json()["fields"]["parent"], self.approved_question.pk)
        self.assertEqual(response.json()["fields"]["creator_id"], self.staff.pk)
        self.assertEqual(response.json()["fields"]["creator_type"], self.user_type.pk)
        self.assertEqual(response.json()["fields"]["approver_id"], None)
        self.assertEqual(response.json()["fields"]["approver_type"], None)
        self.assertEqual(response.json()["fields"]["approved"], False)
        self.assertEqual(response.json()["fields"]["approver_name"], "")
        self.assertEqual(response.json()["fields"]["approver_email"], "")

    def test_update(self):
        url = reverse("thread-detail-update-delete", kwargs={"pk": self.answer.pk})
        url2 = reverse("thread-detail-update-delete", kwargs={"pk": self.question.pk})

        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

        response = self.client.put(
            url, {"title": "testthread"}, content_type="application/json"
        )
        self.assertEqual(response.status_code, 403)

        response = self.staff_client.put(
            url2,
            {
                "title": "testthread 2",
                "approved": True,
                "content": "test",
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["fields"]["title"], "testthread 2")
        self.assertEqual(response.json()["fields"]["content"], "test")
        self.assertEqual(response.json()["fields"]["approved"], True)
        self.assertEqual(response.json()["fields"]["approver_type"], self.user_type.pk)
        self.assertEqual(response.json()["fields"]["approver_id"], self.staff.pk)
        self.assertEqual(
            response.json()["fields"]["approver_name"], self.staff.get_full_name()
        )
        self.assertEqual(response.json()["fields"]["approver_email"], self.staff.email)

        response = self.staff_client.put(
            url,
            {
                "title": "testthread 2",
                "approved": True,
                "content": "test",
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["fields"]["title"], "testthread 2")
        self.assertEqual(response.json()["fields"]["content"], "test")
        self.assertEqual(response.json()["fields"]["approved"], True)
        self.assertEqual(response.json()["fields"]["approver_type"], self.user_type.pk)
        self.assertEqual(response.json()["fields"]["approver_id"], self.staff.pk)
        self.assertEqual(
            response.json()["fields"]["approver_name"], self.staff.get_full_name()
        )
        self.assertEqual(response.json()["fields"]["approver_email"], self.staff.email)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["pk"], self.answer.pk)

        old_parent = self.answer.parent.pk
        new_parent = self.approved_question.pk
        response = self.user_client.put(
            url,
            {
                "title": "testthread 3",
                "parent": new_parent,
                "content": "test",
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["fields"]["title"], "testthread 3")
        self.assertEqual(response.json()["fields"]["content"], "test")
        self.assertEqual(response.json()["fields"]["parent"], old_parent)
        self.assertEqual(response.json()["fields"]["creator_id"], self.user.pk)
        self.assertEqual(response.json()["fields"]["creator_type"], self.user_type.pk)
        self.assertEqual(response.json()["fields"]["approver_id"], None)
        self.assertEqual(response.json()["fields"]["approver_type"], None)
        self.assertEqual(response.json()["fields"]["approved"], False)
        self.assertEqual(response.json()["fields"]["approver_name"], "")
        self.assertEqual(response.json()["fields"]["approver_email"], "")

    def test_delete(self):
        url = reverse("thread-detail-update-delete", kwargs={"pk": self.answer.pk})
        url2 = reverse("thread-detail-update-delete", kwargs={"pk": self.question.pk})

        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)

        response = self.user_client.delete(url)
        self.assertEqual(response.status_code, 204)

        response = self.staff_client.delete(url2)
        self.assertEqual(response.status_code, 204)

    def test_filter_search(self):
        url = reverse("thread-list-create")

        response = self.staff_client.get(url, {"search": "staff"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["results"]), 3)
        self.assertEqual(response.json()["count"], 3)

    def test_filter_created(self):
        url = reverse("thread-list-create")

        response = self.staff_client.get(
            url,
            {
                "created_after": self.created_start,
                "created_before": self.created_end,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["results"]), 1)
        self.assertEqual(response.json()["count"], 1)

    def test_filter_is_question(self):
        url = reverse("thread-list-create")

        response = self.staff_client.get(url, {"is_question": "true"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["results"]), 2)
        self.assertEqual(response.json()["count"], 2)

    def test_filter_is_answer(self):
        url = reverse("thread-list-create")

        response = self.staff_client.get(url, {"is_answer": "true"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["results"]), 2)
        self.assertEqual(response.json()["count"], 2)

    def test_filter_tag_names(self):
        url = reverse("thread-list-create")

        response = self.staff_client.get(url, {"tag_names": "test"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["results"]), 1)
        self.assertEqual(response.json()["count"], 1)

    def test_filter_creator(self):
        url = reverse("thread-list-create")

        response = self.staff_client.get(url, {"creator": self.user.pk})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["results"]), 6)
        self.assertEqual(response.json()["count"], 6)

        response = self.staff_client.get(url, {"creator": 2000})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["results"]), 0)
        self.assertEqual(response.json()["count"], 0)

    def test_filter_approver(self):
        url = reverse("thread-list-create")

        response = self.staff_client.get(url, {"approver": self.staff.pk})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["results"]), 2)
        self.assertEqual(response.json()["count"], 2)

    def test_filter_parent(self):
        url = reverse("thread-list-create")

        response = self.staff_client.get(url, {"parent": self.question.pk})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["results"]), 1)
        self.assertEqual(response.json()["count"], 1)

    def test_filter_order_count_votes(self):
        ThreadVote.objects.create(
            thread=self.question,
            user=self.user,
            is_upvote=True,
        )

        url = reverse("thread-list-create")

        response = self.staff_client.get(url, {"order": "count_votes"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["results"]), 6)
        self.assertEqual(response.json()["count"], 6)
        self.assertEqual(response.json()["results"][-1]["pk"], self.question.pk)

        response = self.staff_client.get(url, {"order": "-count_votes"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["results"]), 6)
        self.assertEqual(response.json()["count"], 6)
        self.assertEqual(response.json()["results"][0]["pk"], self.question.pk)
