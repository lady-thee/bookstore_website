from django.apps import AppConfig
from django.conf import settings
from django.db.models.signals import post_save



class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"

    def ready(self) -> None:
        super().ready()
        from users import signals
        
    # def ready(self) -> None:
    #     super().ready()
    #     post_save.connect(signals.generate_token, sender=settings.AUTH_USER_MODEL)
