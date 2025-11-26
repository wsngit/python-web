from django.apps import AppConfig
import  os


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    def ready(self):
        if not os.environ.get('RUN_MAIN'):
            return
        from .tasks import start_scheduler
        start_scheduler()
