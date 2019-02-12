from django.conf import settings


DEFAULT_MENU_CONFIG = {
    'CURRENT_MENU_ITEM_CLASS': 'current',
    'CURRENT_MENU_ITEM_PARENT_CLASS': 'has-current',
}

existing_conf = getattr(settings, 'NAVUTILS_MENU_CONFIG', {})
DEFAULT_MENU_CONFIG.update(existing_conf)

NAVUTILS_MENU_CONFIG = DEFAULT_MENU_CONFIG

# Template overrides
NAVUTILS_MENU_TEMPLATE = getattr(settings, 'NAVUTILS_MENU_TEMPLATE', 'navutils/menu.html')
NAVUTILS_NODE_TEMPLATE = getattr(settings, 'NAVUTILS_NODE_TEMPLATE', 'navutils/node.html')
NAVUTILS_BREADCRUMBS_TEMPLATE = getattr(settings, 'NAVUTILS_BREADCRUMBS_TEMPLATE', 'navutils/breadcrumbs.html')
NAVUTILS_CRUMB_TEMPLATE = getattr(settings, 'NAVUTILS_CRUMB_TEMPLATE', 'navutils/crumb.html')

