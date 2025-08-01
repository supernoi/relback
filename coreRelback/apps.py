from django.apps import AppConfig


class CorerelbackConfig(AppConfig):
    name = 'coreRelback'

    def ready(self):
        import coreRelback.signals
