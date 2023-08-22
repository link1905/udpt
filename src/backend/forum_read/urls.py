from django.urls import path

from .views import (
    tagged_thread_detail_delete_view,
    tagged_thread_list_create_view,
    thread_detail_update_delete_view,
    thread_list_create_view,
    thread_vote_detail_update_delete_view,
    thread_vote_list_create_view,
    thread_category_list_create_view,
    thread_category_detail_update_delete_view,
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
    path(
        "models/tagged-threads/records/",
        tagged_thread_list_create_view,
        name="tagged-thread-list-create",
    ),
    path(
        "models/tagged-threads/records/<int:pk>/",
        tagged_thread_detail_delete_view,
        name="tagged-thread-detail-delete",
    ),
    path(
        "models/thread-categories/records/",
        thread_category_list_create_view,
        name="thread-category-list-create",
    ),
    path(
        "models/thread-categories/records/<int:pk>/",
        thread_category_detail_update_delete_view,
        name="thread-category-detail-update-delete",
    ),
]

from . import docs as _  # noqa
