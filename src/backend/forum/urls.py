from django.urls import path

from .views import (
    thread_detail_update_delete_view,
    thread_list_create_view,
    thread_vote_detail_update_delete_view,
    thread_vote_list_create_view,
)

urlpatterns = [
    path("models/threads/records/", thread_list_create_view, name="thread-list-create"),
    path(
        "models/threads/records/<int:pk>/",
        thread_detail_update_delete_view,
        name="thread-detail-update-delete",
    ),
    path(
        "models/thread-votes/records/",
        thread_vote_list_create_view,
        name="thread-vote-list-create",
    ),
    path(
        "models/thread-votes/records/<int:pk>/",
        thread_vote_detail_update_delete_view,
        name="thread-vote-detail-update-delete",
    ),
]

from . import docs as _  # noqa
