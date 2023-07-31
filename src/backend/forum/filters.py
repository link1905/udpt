import django_filters
from django.db import models
from forum.models import Thread, ThreadQuerySet


class CharInFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    pass


class ThreadFilterSet(django_filters.FilterSet):
    search = django_filters.CharFilter(field_name="title", lookup_expr="icontains")
    creator = django_filters.NumberFilter(field_name="creator_id", lookup_expr="exact")
    approver = django_filters.NumberFilter(
        field_name="approver_id", lookup_expr="exact"
    )
    parent = django_filters.NumberFilter(field_name="parent_id", lookup_expr="exact")
    created = django_filters.IsoDateTimeFromToRangeFilter()
    is_question = django_filters.BooleanFilter(method="filter_is_question")
    is_answer = django_filters.BooleanFilter(method="filter_is_answer")
    is_pending = django_filters.BooleanFilter(method="filter_is_pending")
    tag_names = CharInFilter(method="filter_tag_names")
    order = django_filters.OrderingFilter(
        fields=(("count_votes", "count_votes"),), method="filter_order"
    )

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

    def filter_tag_names(
        self, queryset: ThreadQuerySet, _: str, value: list[str]
    ) -> ThreadQuerySet:
        return queryset.tag_names(*value)

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

    class Meta:
        model = Thread
        fields = (
            "search",
            "creator",
            "approver",
            "parent",
            "created",
            "is_question",
            "is_answer",
            "is_pending",
            "tag_names",
            "order",
        )


class ThreadVoteFilterSet(django_filters.FilterSet):
    thread = django_filters.NumberFilter(field_name="thread_id", lookup_expr="exact")
    user = django_filters.NumberFilter(field_name="user_id", lookup_expr="exact")
    is_upvote = django_filters.BooleanFilter(
        field_name="is_upvote", lookup_expr="exact"
    )

    class Meta:
        model = Thread
        fields = (
            "thread",
            "user",
            "is_upvote",
        )
