from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"


    def ready(self) -> None:
        super().ready()
        from django.db.models.signals import post_save
        from django.conf import settings
        from  users.signals import generate_token

        post_save.connect(generate_token, sender=settings.AUTH_USER_MODEL)