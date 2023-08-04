from django.http.request import HttpRequest
from django.http.response import HttpResponse, JsonResponse
from django.template import Template
from django.template.context import make_context
from django.urls import path
from django.views.decorators.cache import cache_page

from core.docs import SPEC

@cache_page(31536000)
def docs_json(*_) -> JsonResponse:
    return JsonResponse(SPEC.to_dict())


@cache_page(31536000)
def docs(_: HttpRequest) -> HttpResponse:
    context = make_context(
        {
            "docs_json_url": "./docs.json",
        },
    )

    return HttpResponse(
        content=Template(DOCS_TEMPLATE).render(context=context),
        content_type="text/html",
    )


urlpatterns = [
    path("docs/", docs, name="docs"),
    path("docs/docs.json", docs_json, name="docs-json"),
]


DOCS_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta
      name="description"
      content="SwaggerUI"
    />
    <title>SwaggerUI</title>
    <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@4.5.0/swagger-ui.css" />
  </head>
  <body>
  <div id="swagger-ui"></div>
  <script src="https://unpkg.com/swagger-ui-dist@4.5.0/swagger-ui-bundle.js" crossorigin></script>
  <script src="https://unpkg.com/swagger-ui-dist@4.5.0/swagger-ui-standalone-preset.js" crossorigin></script>
  <script>
    window.onload = () => {
      window.ui = SwaggerUIBundle({
        url: '{{ docs_json_url }}',
        dom_id: '#swagger-ui',
        presets: [
          SwaggerUIBundle.presets.apis,
          SwaggerUIStandalonePreset
        ],
        layout: "StandaloneLayout",
      });
    };
  </script>
  </body>
</html>
"""
