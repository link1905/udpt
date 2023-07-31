from typing import Any, Iterable, Optional, Tuple

from django.db import models
from django.http.request import QueryDict
from django.views.decorators.http import require_http_methods
from djview.auth import USER_CONTEXT_KEY, authentication_layer, is_authenticated_layer
from djview.context import Context
from djview.crud import (
    create_service,
    delete_service,
    detail_service,
    json_parser,
    limit_offset_filterer,
    list_service,
    model_all_filterer,
    model_delete_mutator,
    model_list_serializer,
    model_mutator,
    model_pk_filterer,
    model_serializer,
    model_set_meta_count_filterer,
    multi_part_parser,
    update_service,
    urlencoded_form_parser,
)
from djview.views import (
    case_layer,
    context_view,
    exception_layer,
    from_http_decorator,
    into_service,
    method_layer,
)
from forum.filters import ThreadFilterSet, ThreadVoteFilterSet
from forum.forms import ThreadForm, ThreadStaffForm, ThreadVoteForm
from forum.models import Thread, ThreadVote
from multidbcontenttypes.models import ContentType


def thread_django_filterer(
    ctx: Context, queryset: Optional[Iterable[Any]]
) -> Iterable[Any]:
    return ThreadFilterSet(ctx.request.GET, queryset=queryset, request=ctx.request).qs


def thread_anonymous_filterer(*_: Any) -> Iterable[Any]:
    return Thread.objects.live()


def thread_user_filterer(ctx: Context, _: Optional[Iterable[Any]]) -> Iterable[Any]:
    return Thread.objects.filter(
        Thread.objects.live_q() | models.Q(creator_id=ctx[USER_CONTEXT_KEY].id)
    )


def thread_only_user_filterer(
    ctx: Context, _: Optional[Iterable[Any]]
) -> Iterable[Any]:
    return Thread.objects.filter(models.Q(creator_id=ctx[USER_CONTEXT_KEY].id))


def thread_vote_django_filterer(
    ctx: Context, queryset: Optional[Iterable[Any]]
) -> Iterable[Any]:
    return ThreadVoteFilterSet(
        ctx.request.GET, queryset=queryset, request=ctx.request
    ).qs


def thread_vote_anonymous_filterer(*_: Any) -> Iterable[Any]:
    return ThreadVote.objects.live()


def thread_vote_user_filterer(ctx: Context, *_: Any) -> Iterable[Any]:
    return ThreadVote.objects.filter(
        ThreadVote.objects.live_q() | models.Q(user_id=ctx[USER_CONTEXT_KEY].id)
    )


def thread_vote_only_user_filterer(
    ctx: Context, _: Optional[Iterable[Any]]
) -> Iterable[Any]:
    return ThreadVote.objects.filter(models.Q(user_id=ctx[USER_CONTEXT_KEY].id))


def thread_parser(ctx: Context) -> Optional[Tuple[dict, dict]]:
    data, files = {}, {}
    for parser in (
        json_parser,
        multi_part_parser,
        urlencoded_form_parser,
    ):
        result = parser(ctx)
        if result is None:
            continue

        data, files = result
        break

    if isinstance(data, QueryDict):
        data._mutable = True

    user_type = ContentType.objects.get_for_model(ctx[USER_CONTEXT_KEY])
    data.update(
        {
            "creator_type": user_type.id,
            "creator_id": ctx[USER_CONTEXT_KEY].id,
            "approver_type": user_type.id,
            "approver_id": ctx[USER_CONTEXT_KEY].id,
        }
    )

    if isinstance(data, QueryDict):
        data._mutable = False

    return data, files


def thread_vote_parser(ctx: Context) -> Optional[Tuple[dict, dict]]:
    data, files = {}, {}
    for parser in (
        json_parser,
        multi_part_parser,
        urlencoded_form_parser,
    ):
        result = parser(ctx)
        if result is None:
            continue

        data, files = result
        break

    if isinstance(data, QueryDict):
        data._mutable = True

    user_type = ContentType.objects.get_for_model(ctx[USER_CONTEXT_KEY])
    data.update(
        {
            "user_type": user_type.id,
            "user_id": ctx[USER_CONTEXT_KEY].id,
        }
    )

    if isinstance(data, QueryDict):
        data._mutable = False

    return data, files


thread_list_create_view = context_view()(
    into_service(
        # exception_layer(),
        from_http_decorator(require_http_methods(["GET", "POST"])),
        authentication_layer(),
        method_layer(
            "GET",
            case_layer(
                lambda ctx: not ctx[USER_CONTEXT_KEY].is_authenticated,
                service=list_service(
                    model_list_serializer(),
                    thread_anonymous_filterer,
                    thread_django_filterer,
                    model_set_meta_count_filterer(),
                    limit_offset_filterer(),
                ),
            ),  # anonymous
            case_layer(
                lambda ctx: ctx[USER_CONTEXT_KEY].is_staff
                or ctx[USER_CONTEXT_KEY].is_superuser,
                service=list_service(
                    model_list_serializer(),
                    model_all_filterer(Thread),
                    thread_django_filterer,
                    model_set_meta_count_filterer(),
                    limit_offset_filterer(),
                ),
            ),  # staffs
            service=list_service(
                model_list_serializer(),
                thread_user_filterer,
                thread_django_filterer,
                model_set_meta_count_filterer(),
                limit_offset_filterer(),
            ),  # normal users
        ),
        is_authenticated_layer(),
        service=create_service(
            model_mutator(ThreadForm, thread_parser),
            model_serializer(),
        ),
    )
)

thread_detail_update_delete_view = context_view()(
    into_service(
        exception_layer(),
        from_http_decorator(require_http_methods(["GET", "PUT", "DELETE"])),
        authentication_layer(),
        method_layer(
            "GET",
            case_layer(
                lambda ctx: not ctx[USER_CONTEXT_KEY].is_authenticated,
                service=detail_service(
                    model_serializer(),
                    thread_anonymous_filterer,
                    thread_django_filterer,
                    model_pk_filterer(),
                ),
            ),  # anonymous
            case_layer(
                lambda ctx: ctx[USER_CONTEXT_KEY].is_staff
                or ctx[USER_CONTEXT_KEY].is_superuser,
                service=detail_service(
                    model_serializer(),
                    model_all_filterer(Thread),
                    thread_django_filterer,
                    model_pk_filterer(),
                ),
            ),  # staffs
            service=detail_service(
                model_serializer(),
                thread_user_filterer,
                thread_django_filterer,
                model_pk_filterer(),
            ),  # normal users
        ),
        is_authenticated_layer(),
        method_layer(
            "PUT",
            case_layer(
                lambda ctx: ctx[USER_CONTEXT_KEY].is_staff
                or ctx[USER_CONTEXT_KEY].is_superuser,
                service=update_service(
                    model_mutator(ThreadStaffForm, thread_parser),
                    model_serializer(),
                    model_all_filterer(Thread),
                    thread_django_filterer,
                    model_pk_filterer(),
                ),
            ),  # staffs
            service=update_service(
                model_mutator(ThreadForm, thread_parser),
                model_serializer(),
                thread_only_user_filterer,
                thread_django_filterer,
                model_pk_filterer(),
            ),  # normal users
        ),
        case_layer(
            lambda ctx: ctx[USER_CONTEXT_KEY].is_staff
            or ctx[USER_CONTEXT_KEY].is_superuser,
            service=delete_service(
                model_delete_mutator,
                model_all_filterer(Thread),
                thread_django_filterer,
                model_pk_filterer(),
            ),
        ),  # staffs
        service=delete_service(
            model_delete_mutator,
            thread_only_user_filterer,
            thread_django_filterer,
            model_pk_filterer(),
        ),  # normal users
    )
)

thread_vote_list_create_view = context_view()(
    into_service(
        exception_layer(),
        from_http_decorator(require_http_methods(["GET", "POST"])),
        authentication_layer(),
        method_layer(
            "GET",
            case_layer(
                lambda ctx: not ctx[USER_CONTEXT_KEY].is_authenticated,
                service=list_service(
                    model_list_serializer(),
                    thread_vote_anonymous_filterer,
                    thread_vote_django_filterer,
                    model_set_meta_count_filterer(),
                    limit_offset_filterer(),
                ),
            ),  # staffs
            case_layer(
                lambda ctx: ctx[USER_CONTEXT_KEY].is_staff
                or ctx[USER_CONTEXT_KEY].is_superuser,
                service=list_service(
                    model_list_serializer(),
                    model_all_filterer(ThreadVote),
                    thread_vote_django_filterer,
                    model_set_meta_count_filterer(),
                    limit_offset_filterer(),
                ),
            ),  # staffs
            service=list_service(
                model_list_serializer(),
                thread_vote_user_filterer,
                thread_vote_django_filterer,
                model_set_meta_count_filterer(),
                limit_offset_filterer(),
            ),  # normal users
        ),
        is_authenticated_layer(),
        service=create_service(
            model_mutator(ThreadVoteForm, thread_vote_parser),
            model_serializer(),
        ),
    )
)

thread_vote_detail_update_delete_view = context_view()(
    into_service(
        exception_layer(),
        from_http_decorator(require_http_methods(["GET", "PUT", "DELETE"])),
        authentication_layer(),
        method_layer(
            "GET",
            case_layer(
                lambda ctx: not ctx[USER_CONTEXT_KEY].is_authenticated,
                service=detail_service(
                    model_serializer(),
                    thread_vote_anonymous_filterer,
                    thread_vote_django_filterer,
                    model_pk_filterer(),
                ),
            ),  # staffs
            case_layer(
                lambda ctx: ctx[USER_CONTEXT_KEY].is_staff
                or ctx[USER_CONTEXT_KEY].is_superuser,
                service=detail_service(
                    model_serializer(),
                    model_all_filterer(ThreadVote),
                    thread_vote_django_filterer,
                    model_pk_filterer(),
                ),
            ),  # staffs
            service=detail_service(
                model_serializer(),
                thread_vote_user_filterer,
                thread_vote_django_filterer,
                model_pk_filterer(),
            ),  # normal users
        ),
        is_authenticated_layer(),
        method_layer(
            "PUT",
            case_layer(
                lambda ctx: ctx[USER_CONTEXT_KEY].is_staff
                or ctx[USER_CONTEXT_KEY].is_superuser,
                service=update_service(
                    model_mutator(ThreadVoteForm, thread_vote_parser),
                    model_serializer(),
                    model_all_filterer(ThreadVote),
                    thread_vote_django_filterer,
                    model_pk_filterer(),
                ),
            ),  # staffs
            service=update_service(
                model_mutator(ThreadVoteForm, thread_vote_parser),
                model_serializer(),
                thread_vote_only_user_filterer,
                thread_vote_django_filterer,
                model_pk_filterer(),
            ),  # normal users
        ),
        case_layer(
            lambda ctx: ctx[USER_CONTEXT_KEY].is_staff
            or ctx[USER_CONTEXT_KEY].is_superuser,
            service=delete_service(
                model_delete_mutator,
                model_all_filterer(ThreadVote),
                thread_vote_django_filterer,
                model_pk_filterer(),
            ),
        ),  # staffs
        service=delete_service(
            model_delete_mutator,
            thread_vote_only_user_filterer,
            thread_vote_django_filterer,
            model_pk_filterer(),
        ),  # normal users
    )
)
