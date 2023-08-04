import re

from django.conf import settings
from django.urls import include, path, re_path
from django.views.decorators.cache import cache_page
from django.views.static import serve

urlpatterns = [
    re_path(
        r"^%s(?P<path>.*)$" % re.escape(settings.MEDIA_URL.lstrip("/")),
        cache_page(31536000)(serve),
        kwargs={"document_root": settings.MEDIA_ROOT},
    ),
    path("api/", include("core.docs_urls")),
]

if settings.USE_ACCOUNT_APP:
    urlpatterns += [
        path("api/", include("account.urls")),
    ]

if settings.USE_TAG_APP:
    urlpatterns += [
        path("api/", include("tag.urls")),
    ]

if settings.USE_FORUM_APP:
    urlpatterns += [
        path("api/", include("forum.urls")),
    ]
