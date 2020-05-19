from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = "healthbuddy_backend.users"

    def ready(self):
        from .signals import send_email_recover_password  # noqa: F401
