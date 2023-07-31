from typing import Any

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm as DjangoAuthenticationForm
from django.contrib.auth.forms import PasswordChangeForm as DjangoPasswordChangeForm
from django.contrib.auth.forms import UserChangeForm as DjangoUserChangeForm
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm

User = get_user_model()


class PasswordChangeForm(DjangoPasswordChangeForm):
    def __init__(self, *args: Any, instance: User, **kwargs: Any) -> None:
        super().__init__(instance, *args, **kwargs)


class AuthenticationForm(DjangoAuthenticationForm):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        kwargs.pop("instance", None)
        super().__init__(*args, **kwargs)

    def save(self) -> User:
        return self.get_user()


class UserCreationForm(DjangoUserCreationForm):
    class Meta(DjangoUserCreationForm.Meta):
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "avatar",
            "password1",
            "password2",
        )


class StaffCreationForm(DjangoUserCreationForm):
    class Meta(DjangoUserCreationForm.Meta):
        model = User


class UserChangeForm(DjangoUserChangeForm):
    class Meta(DjangoUserChangeForm.Meta):
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "avatar",
        )


class StaffChangeForm(DjangoUserChangeForm):
    class Meta(DjangoUserChangeForm.Meta):
        model = User
