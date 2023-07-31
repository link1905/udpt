from typing import Any, Iterable, Optional

from django.views.decorators.http import require_http_methods
from djview.context import Context
from djview.crud import (
    detail_service,
    limit_offset_filterer,
    list_service,
    model_all_filterer,
    model_list_serializer,
    model_pk_filterer,
    model_serializer,
    model_set_meta_count_filterer,
)
from djview.views import (
    context_view,
    exception_layer,
    from_http_decorator,
    into_service,
)
from taggit.models import Tag

from .tag_filters import TagFilterSet


def tag_django_filterer(
    ctx: Context, queryset: Optional[Iterable[Any]]
) -> Iterable[Any]:
    return TagFilterSet(ctx.request.GET, queryset=queryset, request=ctx.request).qs


tag_list_view = context_view()(
    into_service(
        exception_layer(),
        from_http_decorator(require_http_methods(["GET"])),
        service=list_service(
            model_list_serializer(),
            model_all_filterer(Tag),
            tag_django_filterer,
            model_set_meta_count_filterer(),
            limit_offset_filterer(),
        ),
    )
)

tag_detail_view = context_view()(
    into_service(
        exception_layer(),
        from_http_decorator(require_http_methods(["GET"])),
        service=detail_service(
            model_serializer(),
            model_all_filterer(Tag),
            tag_django_filterer,
            model_pk_filterer(),
        ),
    )
)
