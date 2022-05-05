import django

from .breadcrumbs import Breadcrumb, BreadcrumbsMixin
from .views import MenuMixin

from . import menu

if django.VERSION < (3, 2):
    default_app_config = 'navutils.apps.App'
