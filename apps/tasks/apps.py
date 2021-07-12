from django.apps import AppConfig
from django.db.models.signals import post_save


class TasksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.tasks'

    def ready(self):
        from apps.tasks.models import Task
        from apps.tasks.signals import on_task_post_save

        post_save.connect(on_task_post_save, sender=Task)
