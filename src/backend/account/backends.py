from typing import Any

from core.jwt import decode_token, new_token
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.http.request import HttpRequest
from djview.views import Optional

User = get_user_model()


class JWTBackend(ModelBackend):
    secret_key = settings.SECRET_KEY
    user_id_field = "id"
    keyword = "Bearer"

    @classmethod
    def get_token(cls, user: User) -> str:
        payload = {
            cls.user_id_field: user.id,
        }
        return new_token(payload, cls.secret_key)

    def authenticate(self, request: HttpRequest = None, **_: Any) -> Optional[User]:
        if not request:
            return None

        token: Optional[str] = request.META.get("HTTP_AUTHORIZATION", None)
        if not token:
            return None

        if token.startswith(self.keyword):
            token = token[len(self.keyword) + 1 :]

        try:
            payload = decode_token(token, self.secret_key)
        except Exception:
            return None

        user_id = payload.get(self.user_id_field, None)
        return self.get_user(user_id)
