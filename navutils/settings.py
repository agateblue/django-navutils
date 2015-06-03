from django.conf import settings


DEFAULT_MENU_CONFIG = {
    'CURRENT_MENU_ITEM_CLASS': 'current',
    'CURRENT_MENU_ITEM_PARENT_CLASS': 'has-current',
}

existing_conf = getattr(settings, 'NAVUTILS_MENU_CONFIG', {})
DEFAULT_MENU_CONFIG.update(existing_conf)

NAVUTILS_MENU_CONFIG = DEFAULT_MENU_CONFIG
