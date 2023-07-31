"""
WSGI config for core project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os
from typing import Any, Callable

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")


def health_check(application: Callable, health_url: str) -> Callable:
    def health_check_wrapper(environ: dict, start_response: Callable) -> Any:
        if environ.get("PATH_INFO") == health_url:
            start_response("200 OK", [("Content-Type", "text/plain")])
            return []
        return application(environ, start_response)

    return health_check_wrapper


application = health_check(get_wsgi_application(), "/health/")
