from typing import Any, Iterable, Optional, Tuple

from account.services import authentication_layer, is_authenticated_layer, is_staff_layer
from django.db import models
from django.http.request import QueryDict
from django.views.decorators.http import require_http_methods
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
from forum.filters import TaggedThreadFilterSet, ThreadCategoryFilterSet, ThreadFilterSet, ThreadVoteFilterSet
from forum.forms import TaggedThreadForm, ThreadCategoryForm, ThreadForm, ThreadStaffForm, ThreadVoteForm
from forum.models import TaggedThread, Thread, ThreadCategory, ThreadVote

USER_CONTEXT_KEY = "__user__"


def thread_django_filterer(
    ctx: Context, queryset: Optional[Iterable[Any]]
) -> Iterable[Any]:
    return ThreadFilterSet(ctx.request.GET, queryset=queryset, request=ctx.request).qs


def thread_anonymous_filterer(*_: Any) -> Iterable[Any]:
    return Thread.objects.live()


def thread_user_filterer(ctx: Context, _: Optional[Iterable[Any]]) -> Iterable[Any]:
    return Thread.objects.filter(
        Thread.objects.live_q() | models.Q(creator_id=ctx[USER_CONTEXT_KEY].pk)
    )


def thread_only_user_filterer(
    ctx: Context, _: Optional[Iterable[Any]]
) -> Iterable[Any]:
    return Thread.objects.filter(models.Q(creator_id=ctx[USER_CONTEXT_KEY].pk))


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
        ThreadVote.objects.live_q() | models.Q(user_id=ctx[USER_CONTEXT_KEY].pk)
    )


def thread_vote_only_user_filterer(
    ctx: Context, _: Optional[Iterable[Any]]
) -> Iterable[Any]:
    return ThreadVote.objects.filter(models.Q(user_id=ctx[USER_CONTEXT_KEY].pk))


def tagged_thread_django_filterer(
    ctx: Context, queryset: Optional[Iterable[Any]]
) -> Iterable[Any]:
    return TaggedThreadFilterSet(
        ctx.request.GET, queryset=queryset, request=ctx.request
    ).qs


def tagged_thread_anonymous_filterer(*_: Any) -> Iterable[Any]:
    return TaggedThread.objects.live()


def tagged_thread_user_filterer(ctx: Context, *_: Any) -> Iterable[Any]:
    return TaggedThread.objects.filter(
        TaggedThread.objects.live_q()
        | models.Q(thread__creator_id=ctx[USER_CONTEXT_KEY].pk)
    )


def tagged_thread_only_user_filterer(
    ctx: Context, _: Optional[Iterable[Any]]
) -> Iterable[Any]:
    return TaggedThread.objects.filter(
        models.Q(thread__creator_id=ctx[USER_CONTEXT_KEY].pk)
    )


def thread_category_django_filterer(
    ctx: Context, queryset: Optional[Iterable[Any]]
) -> Iterable[Any]:
    return ThreadCategoryFilterSet(
        ctx.request.GET, queryset=queryset, request=ctx.request
    ).qs


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

    data.update(
        {
            "creator_id": ctx[USER_CONTEXT_KEY].pk,
            "creator_name": ctx[USER_CONTEXT_KEY].fields.get_full_name(),
            "creator_email": ctx[USER_CONTEXT_KEY].fields.email,
            "approver_id": ctx[USER_CONTEXT_KEY].pk,
            "approver_name": ctx[USER_CONTEXT_KEY].fields.get_full_name(),
            "approver_email": ctx[USER_CONTEXT_KEY].fields.email,
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

    data.update(
        {
            "user_id": ctx[USER_CONTEXT_KEY].pk,
            "user_name": ctx[USER_CONTEXT_KEY].fields.get_full_name(),
            "user_email": ctx[USER_CONTEXT_KEY].fields.email,
        }
    )

    if isinstance(data, QueryDict):
        data._mutable = False

    return data, files


def tagged_thread_parser(ctx: Context) -> Optional[Tuple[dict, dict]]:
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

    data.update({"creator_id": ctx[USER_CONTEXT_KEY].pk})

    if isinstance(data, QueryDict):
        data._mutable = False

    return data, files


thread_list_create_view = context_view()(
    into_service(
        exception_layer(),
        from_http_decorator(require_http_methods(["GET", "POST"])),
        authentication_layer(),
        method_layer(
            "GET",
            case_layer(
                lambda ctx: not ctx[USER_CONTEXT_KEY],
                service=list_service(
                    model_list_serializer(),
                    thread_anonymous_filterer,
                    thread_django_filterer,
                    model_set_meta_count_filterer(),
                    limit_offset_filterer(),
                ),
            ),  # anonymous
            case_layer(
                lambda ctx: ctx[USER_CONTEXT_KEY].fields.is_staff
                or ctx[USER_CONTEXT_KEY].fields.is_superuser,
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
                lambda ctx: not ctx[USER_CONTEXT_KEY],
                service=detail_service(
                    model_serializer(),
                    thread_anonymous_filterer,
                    thread_django_filterer,
                    model_pk_filterer(),
                ),
            ),  # anonymous
            case_layer(
                lambda ctx: ctx[USER_CONTEXT_KEY].fields.is_staff
                or ctx[USER_CONTEXT_KEY].fields.is_superuser,
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
                lambda ctx: ctx[USER_CONTEXT_KEY].fields.is_staff
                or ctx[USER_CONTEXT_KEY].fields.is_superuser,
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
            lambda ctx: ctx[USER_CONTEXT_KEY].fields.is_staff
            or ctx[USER_CONTEXT_KEY].fields.is_superuser,
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
                lambda ctx: not ctx[USER_CONTEXT_KEY],
                service=list_service(
                    model_list_serializer(),
                    thread_vote_anonymous_filterer,
                    thread_vote_django_filterer,
                    model_set_meta_count_filterer(),
                    limit_offset_filterer(),
                ),
            ),  # staffs
            case_layer(
                lambda ctx: ctx[USER_CONTEXT_KEY].fields.is_staff
                or ctx[USER_CONTEXT_KEY].fields.is_superuser,
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
                lambda ctx: not ctx[USER_CONTEXT_KEY],
                service=detail_service(
                    model_serializer(),
                    thread_vote_anonymous_filterer,
                    thread_vote_django_filterer,
                    model_pk_filterer(),
                ),
            ),  # staffs
            case_layer(
                lambda ctx: ctx[USER_CONTEXT_KEY].fields.is_staff
                or ctx[USER_CONTEXT_KEY].fields.is_superuser,
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
                lambda ctx: ctx[USER_CONTEXT_KEY].fields.is_staff
                or ctx[USER_CONTEXT_KEY].fields.is_superuser,
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
            lambda ctx: ctx[USER_CONTEXT_KEY].fields.is_staff
            or ctx[USER_CONTEXT_KEY].fields.is_superuser,
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

tagged_thread_list_create_view = context_view()(
    into_service(
        exception_layer(),
        from_http_decorator(require_http_methods(["GET", "POST"])),
        authentication_layer(),
        method_layer(
            "GET",
            case_layer(
                lambda ctx: not ctx[USER_CONTEXT_KEY],
                service=list_service(
                    model_list_serializer(),
                    tagged_thread_anonymous_filterer,
                    tagged_thread_django_filterer,
                    model_set_meta_count_filterer(),
                    limit_offset_filterer(),
                ),
            ),  # anonymous
            case_layer(
                lambda ctx: ctx[USER_CONTEXT_KEY].fields.is_staff
                or ctx[USER_CONTEXT_KEY].fields.is_superuser,
                service=list_service(
                    model_list_serializer(),
                    model_all_filterer(TaggedThread),
                    tagged_thread_django_filterer,
                    model_set_meta_count_filterer(),
                    limit_offset_filterer(),
                ),
            ),  # staffs
            service=list_service(
                model_list_serializer(),
                tagged_thread_user_filterer,
                tagged_thread_django_filterer,
                model_set_meta_count_filterer(),
                limit_offset_filterer(),
            ),  # normal users
        ),
        is_authenticated_layer(),
        service=create_service(
            model_mutator(TaggedThreadForm, tagged_thread_parser),
            model_serializer(),
        ),
    ),
)


tagged_thread_detail_delete_view = context_view()(
    into_service(
        exception_layer(),
        from_http_decorator(require_http_methods(["GET", "DELETE"])),
        authentication_layer(),
        method_layer(
            "GET",
            case_layer(
                lambda ctx: not ctx[USER_CONTEXT_KEY],
                service=detail_service(
                    model_serializer(),
                    tagged_thread_anonymous_filterer,
                    tagged_thread_django_filterer,
                    model_pk_filterer(),
                ),
            ),  # anonymous
            case_layer(
                lambda ctx: ctx[USER_CONTEXT_KEY].fields.is_staff
                or ctx[USER_CONTEXT_KEY].fields.is_superuser,
                service=detail_service(
                    model_serializer(),
                    model_all_filterer(TaggedThread),
                    tagged_thread_django_filterer,
                    model_pk_filterer(),
                ),
            ),  # staffs
            service=detail_service(
                model_serializer(),
                tagged_thread_user_filterer,
                tagged_thread_django_filterer,
                model_pk_filterer(),
            ),  # normal users
        ),
        is_authenticated_layer(),
        case_layer(
            lambda ctx: ctx[USER_CONTEXT_KEY].fields.is_staff
            or ctx[USER_CONTEXT_KEY].fields.is_superuser,
            service=delete_service(
                model_delete_mutator,
                model_all_filterer(TaggedThread),
                tagged_thread_django_filterer,
                model_pk_filterer(),
            ),
        ),  # staffs
        service=delete_service(
            model_delete_mutator,
            tagged_thread_only_user_filterer,
            tagged_thread_django_filterer,
            model_pk_filterer(),
        ),
    ),
)

thread_category_list_create_view = context_view()(
    into_service(
        exception_layer(),
        from_http_decorator(require_http_methods(["GET", "POST"])),
        authentication_layer(),
        method_layer(
            "GET",
            service=list_service(
                model_list_serializer(),
                model_all_filterer(ThreadCategory),
                thread_category_django_filterer,
                model_set_meta_count_filterer(),
                limit_offset_filterer(),
            ),
        ),
        is_authenticated_layer(),
        is_staff_layer(),
        service=create_service(
            model_mutator(ThreadCategoryForm),
            model_serializer(),
        ),
    ),
)


thread_category_detail_update_delete_view = context_view()(
    into_service(
        exception_layer(),
        from_http_decorator(require_http_methods(["GET", "PUT", "DELETE"])),
        authentication_layer(),
        method_layer(
            "GET",
            service=detail_service(
                model_serializer(),
                model_all_filterer(ThreadCategory),
                thread_category_django_filterer,
                model_pk_filterer(),
            ),
        ),
        is_authenticated_layer(),
        is_staff_layer(),
        method_layer(
            "PUT",
            service=update_service(
                model_mutator(ThreadCategoryForm),
                model_serializer(),
                model_all_filterer(ThreadCategory),
                thread_category_django_filterer,
                model_pk_filterer(),
            ),
        ),
        service=delete_service(
            model_delete_mutator,
            model_all_filterer(ThreadCategory),
            thread_category_django_filterer,
            model_pk_filterer(),
        ),
    )
)


