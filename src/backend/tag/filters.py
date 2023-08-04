import django_filters
from taggit.models import Tag


class CharInFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    pass


class TagFilterSet(django_filters.FilterSet):
    search = django_filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Tag
        fields = ("search",)
