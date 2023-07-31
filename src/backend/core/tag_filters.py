import django_filters
from django.db.models import Exists, OuterRef, QuerySet
from taggit.models import Tag, TaggedItem


class TagFilterSet(django_filters.FilterSet):
    search = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    thread = django_filters.NumberFilter(method="filter_thread")

    def filter_thread(self, queryset: QuerySet, _: str, value: int) -> QuerySet:
        return queryset.filter(
            Exists(
                TaggedItem.objects.filter(
                    content_type__app_label="forum",
                    content_type__model="thread",
                    tag_id=OuterRef("pk"),
                    object_id=value,
                ),
            )
        )

    class Meta:
        model = Tag
        fields = ("thread", "search")
