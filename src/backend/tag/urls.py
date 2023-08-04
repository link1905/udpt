from django.urls import path

from .views import tag_detail_view, tag_list_view

urlpatterns = [
    path("models/tags/records/", tag_list_view, name="tag-list-create"),
    path("models/tags/records/<int:pk>/", tag_detail_view, name="tag-detail"),
]

from . import docs as _  # noqa
