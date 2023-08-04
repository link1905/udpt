from dataclasses import dataclass
from typing import Any, Optional
from urllib.parse import urljoin

import requests
from dataclasses_json import dataclass_json
from django.conf import settings


@dataclass_json
@dataclass
class TagInfo:
    name: str
    slug: str


@dataclass_json
@dataclass
class Tag:
    pk: int
    model: str
    fields: TagInfo


def get_tag(pk: int, **request_options: Any) -> Optional[Tag]:
    base_url = settings.TAG_SERVICE_URL
    url = urljoin(base_url, "models/tags/records/" + str(pk) + "/")
    response = requests.get(url, **request_options)
    if response.status_code != 200:
        return None

    return Tag.from_json(response.content)
