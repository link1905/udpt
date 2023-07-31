from typing import Any

from django.contrib.contenttypes.models import ContentType as DjangoContentType
from django.db.models import Model


class ContentType(DjangoContentType):
    def get_object_for_this_type(self, **kwargs: Any) -> Model:
        return self.model_class()._base_manager.get(**kwargs)

    class Meta:
        proxy = True
