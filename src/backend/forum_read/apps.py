from django.apps import AppConfig


class ForumReadConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "forum_read"

    def ready(self):
        import os
        if os.environ.get('RUN_MAIN') != 'true':
            return
        from .consumer import Consumer
        consumer = Consumer()
        consumer.start_consuming()
