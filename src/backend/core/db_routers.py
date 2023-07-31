from typing import Any, Optional, Type

from django.db.models import Model


class TagRouter:
    route_app_labels = {"taggit", "contenttypes"}
    db_name = "tag"

    def db_for_read(self, model: Type[Model], **_: Any) -> Optional[str]:
        if model._meta.app_label in self.route_app_labels:
            return self.db_name

        return None

    def db_for_write(self, model: Type[Model], **_: Any) -> Optional[str]:
        if model._meta.app_label in self.route_app_labels:
            return self.db_name

        return None

    def allow_relation(self, obj1: Model, obj2: Model, **_: Any) -> Optional[bool]:
        if (
            obj1._meta.app_label in self.route_app_labels
            or obj2._meta.app_label in self.route_app_labels
        ):
            return True

        return None

    def allow_migrate(self, db: str, app_label: str, **_: Any) -> Optional[bool]:
        if app_label in self.route_app_labels and db == self.db_name:
            return True

        return None


class DefaultRouter:
    db_name = "default"

    def db_for_read(self, model: Type[Model], **_: Any) -> Optional[str]:
        return self.db_name

    def db_for_write(self, model: Type[Model], **_: Any) -> Optional[str]:
        return self.db_name

    def allow_relation(self, obj1: Model, obj2: Model, **_: Any) -> Optional[bool]:
        return True

    def allow_migrate(self, db: str, app_label: str, **_: Any) -> Optional[bool]:
        return True
