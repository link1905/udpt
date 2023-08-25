from typing import Callable

from django.http import HttpRequest, HttpResponse


def NonHtmlDebugToolbarMiddleware(
    get_response: Callable[[HttpRequest], HttpResponse]
) -> Callable[[HttpRequest], HttpResponse]:
    def middleware(request: HttpRequest) -> HttpResponse:
        response = get_response(request)

        if request.GET.get("debug"):
            if response["Content-Type"] == "application/json":
                response = HttpResponse(
                    "<html><body><pre>{}</pre></body></html>".format(response.content)
                )

        return response

    return middleware
