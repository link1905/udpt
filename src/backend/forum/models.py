from django.contrib.auth import get_user_model
from django.db import models
from multidbcontenttypes.fields import GenericForeignKey
from multidbcontenttypes.models import ContentType
from taggit.managers import TaggableManager
from taggit.models import TaggedItem

User = get_user_model()


class ThreadQuerySet(models.QuerySet):
    def question_q(_) -> models.Q:
        return models.Q(parent__isnull=True)

    def answer_q(_) -> models.Q:
        return models.Q(parent__isnull=False, parent__parent__isnull=True)

    def comment_q(_) -> models.Q:
        return models.Q(parent__parent__isnull=False)

    # questions are roots
    def questions(self) -> "ThreadQuerySet":
        return self.filter(self.question_q())

    # answers are children of questions
    def answers(self) -> "ThreadQuerySet":
        return self.filter(self.answer_q())

    # comments are children of answers
    def comments(self) -> "ThreadQuerySet":
        return self.filter(self.comment_q())

    def live_q(self) -> models.Q:
        return models.Q(
            (self.question_q() & models.Q(approved=True))
            | (
                self.answer_q()
                & models.Q(approved=True)
                & models.Q(parent__approved=True)
            )
            | (
                self.comment_q()
                & models.Q(parent__approved=True)
                & models.Q(parent__parent__approved=True)
            )
        )

    # live threads are approved questions, answers, and comments
    def live(self) -> "ThreadQuerySet":
        return self.filter(self.live_q())

    # pending threads are unapproved questions, answers
    def pending(self) -> "ThreadQuerySet":
        return self.filter(~self.live_q() & ~self.comment_q())

    # tag_names returns threads that are tagged with all of the given names
    def tag_names(self, *names: str) -> "ThreadQuerySet":
        thread_ids = list(
            TaggedItem.objects.filter(
                content_type__app_label="forum",
                content_type__model="thread",
                tag__name__in=names,
            ).values_list("object_id", flat=True)
        )

        return self.filter(id__in=thread_ids)


class Thread(models.Model):
    title = models.CharField(max_length=255, default="", db_index=True)
    content = models.TextField(db_index=True)

    creator_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, related_name="created_threads"
    )
    creator_id = models.PositiveIntegerField()
    creator = GenericForeignKey("creator_type", "creator_id")

    approver_type = models.ForeignKey(
        ContentType,
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        related_name="approved_threads",
    )
    approver_id = models.PositiveIntegerField(null=True, default=None)
    approver = GenericForeignKey("approver_type", "approver_id")
    approved = models.BooleanField(default=False)
    approver_name = models.CharField(max_length=300, default="")
    approver_email = models.EmailField(default="")

    created = models.DateTimeField(auto_now_add=True, db_index=True)
    updated = models.DateTimeField(auto_now=True, db_index=True)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, related_name="children", null=True, blank=True
    )
    tags = TaggableManager(blank=True)

    objects = ThreadQuerySet.as_manager()

    @property
    def count_upvotes(self) -> int:
        return self.votes.filter(is_upvote=True).count()

    @property
    def count_downvotes(self) -> int:
        return self.votes.filter(is_upvote=False).count()

    class Meta:
        ordering = ["-created"]
        indexes = [
            models.Index(fields=["creator_type", "creator_id"]),
            models.Index(fields=["approver_type", "approver_id"]),
        ]


class ThreadVoteQuerySet(models.QuerySet):
    def live_q(_) -> models.Exists:
        return models.Exists(
            Thread.objects.live().filter(pk=models.OuterRef("thread_id"))
        )

    def live(self) -> "ThreadVoteQuerySet":
        return self.filter(self.live_q())


class ThreadVote(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name="votes")

    user_type = models.ForeignKey(
        ContentType, on_delete=models.SET_NULL, null=True, related_name="thread_votes"
    )
    user_id = models.PositiveIntegerField(null=True, default=None)
    user = GenericForeignKey("user_type", "user_id")
    user_name = models.CharField(max_length=300)
    user_email = models.EmailField()

    is_upvote = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    updated = models.DateTimeField(auto_now=True, db_index=True)

    objects = ThreadVoteQuerySet.as_manager()

    class Meta:
        ordering = ["-created"]
        unique_together = ("thread", "user_type", "user_id")
        indexes = [
            models.Index(fields=["user_type", "user_id"]),
        ]
