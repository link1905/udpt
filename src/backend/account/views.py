import json
from typing import Any, Dict, Iterable, Optional, Tuple

from account.backends import JWTBackend
from account.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    StaffChangeForm,
    StaffCreationForm,
    UserChangeForm,
    UserCreationForm,
)
from django.contrib.auth import get_user_model
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.http.response import HttpResponse
from django.views.decorators.http import require_http_methods
from djview.auth import USER_CONTEXT_KEY, authentication_layer, is_authenticated_layer
from djview.context import Context
from djview.crud import (
    META_CONTEXT_KEY,
    create_service,
    delete_service,
    detail_service,
    limit_offset_filterer,
    list_service,
    model_all_filterer,
    model_delete_mutator,
    model_list_serializer,
    model_mutator,
    model_pk_filterer,
    model_serializer,
    model_set_meta_count_filterer,
    update_service,
)
from djview.views import (
    case_layer,
    context_view,
    exception_layer,
    from_http_decorator,
    into_service,
    method_layer,
)

User = get_user_model()

USER_EXPOSED_FIELDS = (
    "username",
    "first_name",
    "last_name",
    "email",
    "is_staff",
    "is_active",
    "date_joined",
    "last_login",
    "is_superuser",
    "avatar",
)


def login_serializer(_: Context, user: Any) -> Tuple[str, Any]:
    token = JWTBackend.get_token(user)

    return "application/json", json.dumps(
        {
            "token": token,
            "user": serializers.serialize("python", [user], fields=USER_EXPOSED_FIELDS)[
                0
            ],
        },
        cls=DjangoJSONEncoder,
    )


def user_self_filterer(ctx: Context, _: Optional[Iterable[Any]]) -> Iterable[Any]:
    meta: Dict[str, Any] = ctx.get(META_CONTEXT_KEY, {})
    meta["count"] = 1
    ctx[META_CONTEXT_KEY] = meta

    return [ctx[USER_CONTEXT_KEY]]


def auth_refresh_service(ctx: Context) -> HttpResponse:
    user = ctx[USER_CONTEXT_KEY]
    content_type, content = login_serializer(ctx, user)
    return HttpResponse(content, content_type=content_type)


login_view = context_view()(
    into_service(
        exception_layer(),
        from_http_decorator(require_http_methods(["POST"])),
        service=create_service(
            model_mutator(AuthenticationForm),
            login_serializer,
        ),
    )
)


auth_refresh_view = context_view()(
    into_service(
        exception_layer(),
        from_http_decorator(require_http_methods(["POST"])),
        authentication_layer(),
        is_authenticated_layer(),
        service=auth_refresh_service,
    )
)

password_change_view = context_view()(
    into_service(
        exception_layer(),
        from_http_decorator(require_http_methods(["POST"])),
        authentication_layer(),
        is_authenticated_layer(),
        service=update_service(
            model_mutator(PasswordChangeForm),
            model_serializer(fields=USER_EXPOSED_FIELDS),
            user_self_filterer,
        ),
    )
)

user_list_create_view = context_view()(
    into_service(
        exception_layer(),
        from_http_decorator(require_http_methods(["GET", "POST"])),
        authentication_layer(),
        method_layer(
            "GET",
            is_authenticated_layer(),
            case_layer(
                lambda ctx: ctx[USER_CONTEXT_KEY].is_staff
                or ctx[USER_CONTEXT_KEY].is_superuser,
                service=list_service(
                    model_list_serializer(fields=USER_EXPOSED_FIELDS),
                    model_all_filterer(User),
                    model_set_meta_count_filterer(),
                    limit_offset_filterer(),
                ),
            ),  # staffs
            service=list_service(
                model_list_serializer(fields=USER_EXPOSED_FIELDS),
                user_self_filterer,
                limit_offset_filterer(),
            ),  # normal users
        ),
        case_layer(
            lambda ctx: ctx[USER_CONTEXT_KEY].is_authenticated
            and (ctx[USER_CONTEXT_KEY].is_staff or ctx[USER_CONTEXT_KEY].is_superuser),
            service=create_service(
                model_mutator(StaffCreationForm),
                model_serializer(fields=USER_EXPOSED_FIELDS),
            ),
        ),
        service=create_service(
            model_mutator(UserCreationForm),
            model_serializer(fields=USER_EXPOSED_FIELDS),
        ),
    )
)

user_detail_update_delete_view = context_view()(
    into_service(
        exception_layer(),
        from_http_decorator(require_http_methods(["GET", "PUT", "DELETE"])),
        authentication_layer(),
        is_authenticated_layer(),
        method_layer(
            "GET",
            case_layer(
                lambda ctx: ctx[USER_CONTEXT_KEY].is_staff
                or ctx[USER_CONTEXT_KEY].is_superuser,
                service=detail_service(
                    model_serializer(fields=USER_EXPOSED_FIELDS),
                    model_all_filterer(User),
                    model_pk_filterer(),
                ),
            ),  # staffs
            service=detail_service(
                model_serializer(fields=USER_EXPOSED_FIELDS),
                user_self_filterer,
            ),  # normal users
        ),
        method_layer(
            "PUT",
            case_layer(
                lambda ctx: ctx[USER_CONTEXT_KEY].is_staff
                or ctx[USER_CONTEXT_KEY].is_superuser,
                service=update_service(
                    model_mutator(StaffChangeForm),
                    model_serializer(fields=USER_EXPOSED_FIELDS),
                    model_all_filterer(User),
                    model_pk_filterer(),
                ),
            ),  # staffs
            service=update_service(
                model_mutator(UserChangeForm),
                model_serializer(fields=USER_EXPOSED_FIELDS),
                user_self_filterer,
            ),  # normal users
        ),
        case_layer(
            lambda ctx: ctx[USER_CONTEXT_KEY].is_staff
            or ctx[USER_CONTEXT_KEY].is_superuser,
            service=delete_service(
                model_delete_mutator,
                model_all_filterer(User),
                model_pk_filterer(),
            ),
        ),  # staffs
        service=delete_service(
            model_delete_mutator,
            user_self_filterer,
        ),
    )
)
