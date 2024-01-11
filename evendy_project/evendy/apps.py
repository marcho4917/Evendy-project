from django.apps import AppConfig


class EvendyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'evendy'

    def ready(self):
        import evendy.signals
        