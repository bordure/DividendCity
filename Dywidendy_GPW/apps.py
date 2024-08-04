from django.apps import AppConfig

class DywidendyGpwConfig(AppConfig):
    name = 'Dywidendy_GPW'

    def ready(self):
        import Dywidendy_GPW.signals
