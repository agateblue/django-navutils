from django import template
from navutils import settings

register = template.Library()


@register.simple_tag(takes_context=True)
def render_menu(context, menu, **kwargs):

    # menu = kwargs.get('menu', context.get('menu'))
    # if not menu:
    #     raise ValueError('Missing menu argument')

    user = kwargs.get('user', context.get('user', getattr(context.get('request', object()), 'user', None)))
    if not user:
        raise ValueError('missing user parameter')

    max_depth = kwargs.get('max_depth', context.get('max_depth', 999))
    viewable_nodes = [node for node in menu.values() if node.is_viewable_by(user, context)]
    if not viewable_nodes:
        return ''

    t = template.loader.get_template(menu.template)
    c = {
        'menu': menu,
        'viewable_nodes': viewable_nodes,
        'user': user,
        'max_depth': max_depth,
        'current_menu_item': kwargs.get('current_menu_item', context.get('current_menu_item')),
        'menu_config': settings.NAVUTILS_MENU_CONFIG
    }

    context.update(c)
    final_context = menu.get_context(context)
    return t.render(template.Context(final_context))

@register.simple_tag(takes_context=True)
def render_node(context, node, **kwargs):
    # node = kwargs.get('node', context.get('node'))
    # if not node:
    #     raise ValueError('Missing node argument')


    user = kwargs.get('user', context.get('user', getattr(context.get('request', object()), 'user', None)))
    if not user:
        raise ValueError('missing user parameter')

    if not node.is_viewable_by(user, context):
        return ''

    current = kwargs.get('current_menu_item', context.get('current_menu_item'))
    max_depth = kwargs.get('max_depth', context.get('max_depth', 999))
    start_depth = kwargs.get('start_depth', context.get('start_depth', node.depth))
    current_depth = kwargs.get('current_depth', context.get('current_depth', node.depth - start_depth))

    viewable_children = []
    if current_depth + 1 <= max_depth:
        for child in node.children:
            if child.is_viewable_by(user, context):
                viewable_children.append(child)

    t = template.loader.get_template(node.template)

    c = {
        'is_current': node.is_current(current),
        'has_current': node.has_current(current, viewable_children),
        'current_menu_item': current,
        'node': node,
        'viewable_children': viewable_children,
        'user': user,
        'max_depth': max_depth,
        'current_depth': current_depth,
        'start_depth': start_depth,
        'menu_config': settings.NAVUTILS_MENU_CONFIG
    }
    context.update(c)
    final_context = node.get_context(context)

    return t.render(template.Context(final_context))


@register.simple_tag(takes_context=True)
def render_crumb(context, crumb, **kwargs):

    t = template.loader.get_template('navutils/crumb.html')

    return t.render(template.Context({
        'crumb': crumb,
        'last': kwargs.get('last', False),
    }))

@register.simple_tag(takes_context=True)
def render_breadcrumbs(context, crumbs, **kwargs):

    t = template.loader.get_template('navutils/breadcrumbs.html')

    return t.render(template.Context({
        'crumbs': crumbs,
    }))
