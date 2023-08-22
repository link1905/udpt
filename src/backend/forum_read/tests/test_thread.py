from account.test import LiveServerAuthenticatedTestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from forum.models import TaggedThread, Thread, ThreadCategory, ThreadVote
from taggit.models import Tag

User = get_user_model()


class TestThreadAPI(LiveServerAuthenticatedTestCase):
    def setUp(self) -> None:
        super().setUp()
        
        self.category = ThreadCategory.objects.create(name="testcategory")
        self.category2 = ThreadCategory.objects.create(name="testcategory2")

        self.tag1 = Tag.objects.create(name="tag1")
        self.tag2 = Tag.objects.create(name="tag2")

        self.question = Thread.objects.create(
            title="testthread",
            content="test",
            creator_id=self.user.id,
            creator_name=self.user.get_full_name(),
            creator_email=self.user.email,
            category=self.category,
        )
        TaggedThread.objects.create(
            thread=self.question,
            tag_id=self.tag1.pk,
        )
        self.answer = Thread.objects.create(
            title="testthread",
            content="test",
            parent=self.question,
            creator_id=self.user.id,
            creator_name=self.user.get_full_name(),
            creator_email=self.user.email,
        )
        Thread.objects.create(
            title="testthread",
            content="test",
            parent=self.answer,
            creator_id=self.user.id,
            creator_name=self.user.get_full_name(),
            creator_email=self.user.email,
        )

        self.created_start = timezone.now()
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
            category=self.category2,
        )
        TaggedThread.objects.create(
            thread=self.approved_question,
            tag_id=self.tag2.pk,
        )
        self.created_end = timezone.now()
        self.approved_answer = Thread.objects.create(
            title="testthread staff",
            content="test",
            creator_id=self.user.id,
            creator_name=self.user.get_full_name(),
            creator_email=self.user.email,
            parent=self.approved_question,
            approved=True,
            approver_id=self.staff.id,
            approver_name=self.staff.get_full_name(),
            approver_email=self.staff.email,
        )
        Thread.objects.create(
            title="testthread staff",
            content="test",
            creator_id=self.user.id,
            creator_name=self.user.get_full_name(),
            creator_email=self.user.email,
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
                "category": self.category.pk,
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
        self.assertEqual(response.json()["fields"]["approver_id"], 0)
        self.assertEqual(response.json()["fields"]["approved"], False)
        self.assertEqual(response.json()["fields"]["approver_name"], "")
        self.assertEqual(response.json()["fields"]["approver_email"], "")

        response = self.user_client.post(
            url,
            {
                "title": "testthread2",
                "content": "test",
                "category": self.category2.pk,
            },
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["fields"]["title"], "testthread2")
        self.assertEqual(response.json()["fields"]["content"], "test")
        self.assertEqual(response.json()["fields"]["parent"], None)
        self.assertEqual(response.json()["fields"]["creator_id"], self.user.pk)
        self.assertEqual(response.json()["fields"]["approver_id"], 0)
        self.assertEqual(response.json()["fields"]["approved"], False)
        self.assertEqual(response.json()["fields"]["approver_name"], "")
        self.assertEqual(response.json()["fields"]["approver_email"], "")
        self.assertEqual(response.json()["fields"]["category"], self.category2.pk)

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
        self.assertEqual(response.json()["fields"]["approver_id"], 0)
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
        self.assertEqual(response.json()["fields"]["approver_id"], 0)
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

    def test_filter_tag_ids(self):
        url = reverse("thread-list-create")

        tag = self.tag1

        response = self.staff_client.get(url, {"tag_ids": tag.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["results"]), 1)
        self.assertEqual(response.json()["count"], 1)

    def test_filter_creator_id(self):
        url = reverse("thread-list-create")

        response = self.staff_client.get(url, {"creator_id": self.user.pk})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["results"]), 6)
        self.assertEqual(response.json()["count"], 6)

        response = self.staff_client.get(url, {"creator_id": 2000})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["results"]), 0)
        self.assertEqual(response.json()["count"], 0)

    def test_filter_approver_id(self):
        url = reverse("thread-list-create")

        response = self.staff_client.get(url, {"approver_id": self.staff.pk})
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
            user_id=self.user.pk,
            user_name=self.user.get_full_name(),
            user_email=self.user.email,
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

    def test_filter_category(self):
        url = reverse("thread-list-create")

        response = self.staff_client.get(url, {"category": self.category.pk})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["results"]), 3)
        self.assertEqual(response.json()["count"], 3)
