from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


from .producer import *


def on_saved(instance, created, get_serializer, model_name):
    serializer = get_serializer(instance)
    print('saved', model_name, serializer.data)
    publish(f'{model_name}_saved', serializer.data)
    return instance


def on_deleted(instance, get_serializer, model_name):
    serializer = get_serializer(instance)
    print('deleted', model_name, serializer.data)
    publish(f'{model_name}_deleted', serializer.data)


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

    def category(self, category_id: int) -> "ThreadQuerySet":
        return self.filter(
            (self.question_q() & models.Q(category_id=category_id))
            | (self.answer_q() & models.Q(parent__category_id=category_id))
            | models.Q(parent__parent__category_id=category_id)
        )


class ThreadCategory(models.Model):
    name = models.CharField(max_length=300, unique=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    updated = models.DateTimeField(auto_now=True, db_index=True)


@receiver(post_save, sender=ThreadCategory)
def on_thread_category_created(sender, instance, created, **kwargs):
    from .serializers import ThreadCategorySerializer
    on_saved(instance, created, lambda x: ThreadCategorySerializer(x), "thread_category")
    return instance


@receiver(post_delete, sender=ThreadCategory)
def on_thread_category_deleted(sender, instance, **kwargs):
    from .serializers import ThreadCategorySerializer
    on_deleted(instance, lambda x: ThreadCategorySerializer(x), "thread_category")
    return instance


class Thread(models.Model):
    title = models.CharField(max_length=255, default="", db_index=True)
    content = models.TextField(db_index=True)
    category = models.ForeignKey(ThreadCategory, on_delete=models.CASCADE, null=True, blank=True, related_name="threads")

    creator_id = models.PositiveIntegerField(db_index=True)
    creator_name = models.CharField(max_length=300, default="", blank=True)
    creator_email = models.EmailField(default="", blank=True)

    approver_id = models.PositiveIntegerField(db_index=True, default=0, blank=True)
    approved = models.BooleanField(default=False, blank=True)
    approver_name = models.CharField(max_length=300, default="", blank=True)
    approver_email = models.EmailField(default="", blank=True)

    created = models.DateTimeField(auto_now_add=True, db_index=True)
    updated = models.DateTimeField(auto_now=True, db_index=True)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, related_name="children", null=True, blank=True
    )

    objects = ThreadQuerySet.as_manager()

    @property
    def count_upvotes(self) -> int:
        return self.votes.filter(is_upvote=True).count()

    @property
    def count_downvotes(self) -> int:
        return self.votes.filter(is_upvote=False).count()

    class Meta:
        ordering = ["-created"]


@receiver(post_save, sender=Thread)
def on_thread_created(sender, instance, created, **kwargs):
    from .serializers import ThreadSerializer
    on_saved(instance, created, lambda x: ThreadSerializer(x), "thread")
    return instance


@receiver(post_delete, sender=Thread)
def on_thread_deleted(sender, instance, **kwargs):
    from .serializers import ThreadSerializer
    on_deleted(instance, lambda x: ThreadSerializer(x), "thread")
    return instance


class ThreadVoteQuerySet(models.QuerySet):
    def live_q(_) -> models.Exists:
        return models.Exists(
            Thread.objects.live().filter(pk=models.OuterRef("thread_id"))
        )

    def live(self) -> "ThreadVoteQuerySet":
        return self.filter(self.live_q())


class ThreadVote(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name="votes")

    user_id = models.PositiveIntegerField(db_index=True)
    user_name = models.CharField(max_length=300, default="", blank=True)
    user_email = models.EmailField(default="", blank=True)

    is_upvote = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    updated = models.DateTimeField(auto_now=True, db_index=True)

    objects = ThreadVoteQuerySet.as_manager()

    class Meta:
        ordering = ["-created"]
        unique_together = ("thread", "user_id")


@receiver(post_save, sender=ThreadVote)
def on_thread_vote_created(sender, instance, created, **kwargs):
    from .serializers import ThreadVoteSerializer
    on_saved(instance, created, lambda x: ThreadVoteSerializer(x), "thread_vote")
    return instance


@receiver(post_delete, sender=ThreadVote)
def on_thread_vote_deleted(sender, instance, **kwargs):
    from .serializers import ThreadVoteSerializer
    on_deleted(instance, lambda x: ThreadVoteSerializer(x), "thread_vote")
    return instance


class TaggedThreadQuerySet(models.QuerySet):
    def live_q(_) -> models.Exists:
        return models.Exists(
            Thread.objects.live().filter(pk=models.OuterRef("thread_id"))
        )

    def live(self) -> "ThreadVoteQuerySet":
        return self.filter(self.live_q())


class TaggedThread(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name="tags")
    tag_id = models.PositiveIntegerField(db_index=True)
    tag_name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    updated = models.DateTimeField(auto_now=True, db_index=True)

    objects = TaggedThreadQuerySet.as_manager()

    class Meta:
        unique_together = ("thread", "tag_id")



@receiver(post_save, sender=TaggedThread)
def on_thread_vote_created(sender, instance, created, **kwargs):
    from .serializers import TaggedThreadSerializer
    on_saved(instance, created, lambda x: TaggedThreadSerializer(x), "thread_tag")
    return instance


@receiver(post_delete, sender=TaggedThread)
def on_thread_vote_deleted(sender, instance, **kwargs):
    from .serializers import TaggedThreadSerializer
    on_deleted(instance, lambda x: TaggedThreadSerializer(x), "thread_tag")
    return instance
