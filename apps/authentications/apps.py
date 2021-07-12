from django.apps import AppConfig
from django.db.models.signals import post_save


class AuthenticationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.authentications'

    def ready(self):
        from apps.authentications.models import User
        from apps.authentications.signals import create_auth_token

        post_save.connect(create_auth_token, sender=User)
