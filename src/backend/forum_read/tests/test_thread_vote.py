from account.test import LiveServerAuthenticatedTestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from forum.models import Thread, ThreadVote

User = get_user_model()


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

        self.vote = ThreadVote.objects.create(
            thread=self.question,
            user_id=self.user.id,
            user_name=self.user.get_full_name(),
            user_email=self.user.email,
            is_upvote=False,
        )
        self.vote2 = ThreadVote.objects.create(
            thread=self.question,
            user_id=self.staff.id,
            user_name=self.staff.get_full_name(),
            user_email=self.staff.email,
            is_upvote=False,
        )
        self.approved_vote = ThreadVote.objects.create(
            thread=self.approved_question,
            user_id=self.user.id,
            user_name=self.user.get_full_name(),
            user_email=self.user.email,
        )

    def test_list(self):
        url = reverse("thread-vote-list-create")

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["results"]), 1)

        response = self.user_client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["results"]), 2)

        response = self.staff_client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["results"]), 3)

    def test_detail(self):
        url = reverse("thread-vote-detail-update-delete", kwargs={"pk": self.vote.pk})
        url2 = reverse(
            "thread-vote-detail-update-delete", kwargs={"pk": self.approved_vote.pk}
        )

        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

        response = self.client.get(url2)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["pk"], self.approved_vote.pk)

        response = self.user_client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["pk"], self.vote.pk)

        response = self.staff_client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["pk"], self.vote.pk)

    def test_create(self):
        ThreadVote.objects.all().delete()

        url = reverse("thread-vote-list-create")

        response = self.client.post(
            url, {"thread": self.question.pk}, content_type="application/json"
        )
        self.assertEqual(response.status_code, 403)

        response = self.user_client.post(
            url, {"thread": self.question.pk}, content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

        response = self.user_client.post(
            url, {"thread": self.approved_question.pk}, content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["fields"]["thread"], self.approved_question.pk)
        self.assertEqual(response.json()["fields"]["user_id"], self.user.pk)
        self.assertEqual(
            response.json()["fields"]["user_name"], self.user.get_full_name()
        )
        self.assertEqual(response.json()["fields"]["user_email"], self.user.email)

        response = self.user_client.post(
            url, {"thread": self.approved_question.pk}, content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    def test_update(self):
        url = reverse(
            "thread-vote-detail-update-delete", kwargs={"pk": self.approved_vote.pk}
        )

        response = self.client.put(
            url, {"thread": self.question.pk}, content_type="application/json"
        )
        self.assertEqual(response.status_code, 403)

        response = self.user_client.put(
            url,
            {
                "thread": self.question.pk,
                "is_upvote": False,
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["fields"]["thread"], self.approved_question.pk)
        self.assertEqual(response.json()["fields"]["is_upvote"], False)

        response = self.staff_client.put(
            url,
            {
                "thread": self.question.pk,
                "is_upvote": True,
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["fields"]["thread"], self.approved_question.pk)
        self.assertEqual(response.json()["fields"]["is_upvote"], True)

    def test_delete(self):
        url = reverse(
            "thread-vote-detail-update-delete", kwargs={"pk": self.approved_vote.pk}
        )
        url2 = reverse("thread-vote-detail-update-delete", kwargs={"pk": self.vote.pk})

        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)

        response = self.user_client.delete(url)
        self.assertEqual(response.status_code, 204)

        response = self.staff_client.delete(url2)
        self.assertEqual(response.status_code, 204)

    def test_filter_thread(self):
        url = reverse("thread-vote-list-create")

        response = self.staff_client.get(url, {"thread": self.question.pk})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["results"]), 2)

    def test_filter_user(self):
        url = reverse("thread-vote-list-create")

        response = self.staff_client.get(url, {"user_id": self.user.pk})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["results"]), 2)

    def test_filter_is_upvote(self):
        url = reverse("thread-vote-list-create")

        response = self.staff_client.get(url, {"is_upvote": "false"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["results"]), 2)
