from dataclasses import dataclass, field
from datetime import datetime
from functools import wraps
from typing import Any, Callable, Optional
from urllib.parse import urljoin

import requests
from dataclasses_json import config, dataclass_json
from django.conf import settings
from django.http.response import HttpResponseBase
from djview.context import Context
from djview.views import Layer, Service, case_layer, view403
from marshmallow import fields

USER_CONTEXT_KEY = "__user__"


@dataclass_json
@dataclass
class UserInfo:
    username: str
    first_name: str
    last_name: str
    email: str
    is_staff: bool
    is_active: bool
    date_joined: datetime = field(
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat,
            mm_field=fields.DateTime(format="iso"),
        )
    )
    avatar: str
    is_superuser: bool
    last_login: Optional[datetime] = field(
        default=None,
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat,
            mm_field=fields.DateTime(format="iso"),
            exclude=lambda x: x is None,
        ),
    )

    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


@dataclass_json
@dataclass
class User:
    pk: int
    model: str
    fields: UserInfo


@dataclass_json
@dataclass
class AuthRefreshResponse:
    token: str
    user: User


def authenticate(token: str, **request_options: Any) -> Optional[User]:
    base_url = settings.ACCOUNT_SERVICE_URL
    url = urljoin(base_url, "models/users/auth-refresh/")
    response = requests.post(url, headers={"Authorization": token}, **request_options)

    if response.status_code != 200:
        return None

    return AuthRefreshResponse.from_json(response.content).user


def permission_layer(*rules: Callable[[Context], bool]) -> Layer:
    return case_layer(
        lambda ctx: any((not rule(ctx) for rule in rules)),
        service=view403,
    )


def authentication_layer(user_ctx_key: str = USER_CONTEXT_KEY) -> Layer:
    def inner(service: Service) -> Service:
        @wraps(service)
        def wrapper(ctx: Context) -> HttpResponseBase:
            token = ctx.request.META.get("HTTP_AUTHORIZATION", "")
            ctx[user_ctx_key] = authenticate(token)

            return service(ctx)

        return wrapper

    return inner


def is_authenticated_layer(user_ctx_key: str = USER_CONTEXT_KEY) -> Layer:
    def rule(ctx: Context) -> bool:
        return ctx[user_ctx_key] is not None

    return permission_layer(rule)


def is_staff_layer(user_ctx_key: str = USER_CONTEXT_KEY) -> Layer:
    def rule(ctx: Context) -> bool:
        return ctx[user_ctx_key].fields.is_staff

    return permission_layer(rule)
