import django_filters
from django.db import models
from forum.models import TaggedThread, Thread, ThreadQuerySet, ThreadCategory


class CharInFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    pass


class ThreadFilterSet(django_filters.FilterSet):
    search = django_filters.CharFilter(field_name="title", lookup_expr="icontains")
    creator_id = django_filters.NumberFilter(
        field_name="creator_id", lookup_expr="exact"
    )
    approver_id = django_filters.NumberFilter(
        field_name="approver_id", lookup_expr="exact"
    )
    parent = django_filters.NumberFilter(field_name="parent_id", lookup_expr="exact")
    created = django_filters.IsoDateTimeFromToRangeFilter()
    is_question = django_filters.BooleanFilter(method="filter_is_question")
    is_answer = django_filters.BooleanFilter(method="filter_is_answer")
    is_pending = django_filters.BooleanFilter(method="filter_is_pending")
    tag_ids = CharInFilter(field_name="tags__tag_id")
    order = django_filters.OrderingFilter(
        fields=(("count_votes", "count_votes"),), method="filter_order"
    )
    category = django_filters.NumberFilter(method="filter_category")

    def filter_is_question(
        self, queryset: ThreadQuerySet, _: str, value: bool
    ) -> ThreadQuerySet:
        return queryset.filter(
            queryset.question_q() if value else ~queryset.question_q()
        )

    def filter_is_answer(
        self, queryset: ThreadQuerySet, _: str, value: bool
    ) -> ThreadQuerySet:
        return queryset.filter(queryset.answer_q() if value else ~queryset.answer_q())

    def filter_is_pending(
        self, queryset: ThreadQuerySet, _: str, value: bool
    ) -> ThreadQuerySet:
        return queryset.pending() if value else queryset.live()

    def filter_order(
        self, queryset: ThreadQuerySet, _: str, value: list[str]
    ) -> ThreadQuerySet:
        for v in value:
            if "count_votes" in v:
                queryset = queryset.annotate(
                    count_votes=(
                        models.Count("votes", filter=models.Q(votes__is_upvote=True))
                        - models.Count("votes", filter=models.Q(votes__is_upvote=False))
                    )
                )

        # prevent infinite recursion
        self.filters["order"].method = None
        try:
            queryset = self.filters["order"].filter(queryset, value)
        finally:
            self.filters["order"].method = "filter_order"

        return queryset

    def filter_category(self, queryset: ThreadQuerySet, _: str, value: int) -> ThreadQuerySet:
        return queryset.category(value)

    class Meta:
        model = Thread
        fields = (
            "search",
            "creator_id",
            "approver_id",
            "parent",
            "created",
            "is_question",
            "is_answer",
            "is_pending",
            "tag_ids",
            "order",
            "category",
        )


class ThreadVoteFilterSet(django_filters.FilterSet):
    thread = django_filters.NumberFilter(field_name="thread_id", lookup_expr="exact")
    user_id = django_filters.NumberFilter(field_name="user_id", lookup_expr="exact")
    is_upvote = django_filters.BooleanFilter(
        field_name="is_upvote", lookup_expr="exact"
    )

    class Meta:
        model = Thread
        fields = (
            "thread",
            "user_id",
            "is_upvote",
        )


class TaggedThreadFilterSet(django_filters.FilterSet):
    tag_id = django_filters.NumberFilter(field_name="tag_id", lookup_expr="exact")
    thread = django_filters.NumberFilter(field_name="thread_id", lookup_expr="exact")

    class Meta:
        model = TaggedThread
        fields = (
            "tag_id",
            "thread",
        )

class ThreadCategoryFilterSet(django_filters.FilterSet):
    search = django_filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = ThreadCategory
        fields = (
            "search",
        )
