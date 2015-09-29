from django.apps import AppConfig

from django.conf import settings

class App(AppConfig):
    name = 'navutils'

    def ready(self):
        from . import menu
        menu.registry.autodiscover(settings.INSTALLED_APPS)
