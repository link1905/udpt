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
    path("api/", include("core.tag_urls")),
    path("api/", include("core.docs_urls")),
    path("api/", include("account.urls")),
    path("api/", include("forum.urls")),
]
