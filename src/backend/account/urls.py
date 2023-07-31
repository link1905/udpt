from django.urls import path

from .views import (
    auth_refresh_view,
    login_view,
    password_change_view,
    user_detail_update_delete_view,
    user_list_create_view,
)

urlpatterns = [
    path("models/users/login/", login_view, name="login"),
    path("models/users/auth-refresh/", auth_refresh_view, name="auth-refresh"),
    path("models/users/change-password/", password_change_view, name="change-password"),
    path("models/users/records/", user_list_create_view, name="user-list-create"),
    path(
        "models/users/records/<int:pk>/",
        user_detail_update_delete_view,
        name="user-detail-update-delete",
    ),
]

from . import docs as _  # noqa
