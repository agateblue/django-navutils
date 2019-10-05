from django.apps import AppConfig, apps


class App(AppConfig):
    name = 'navutils'

    def ready(self):
        from . import menu
        menu.registry.autodiscover((a.name for a in apps.get_app_configs()))
