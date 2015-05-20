from . import menu


def menus(*args, **kwargs):
    return {'menus': menu.registry}
