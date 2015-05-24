from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def render_menu(context, menu, user, max_depth=999, **kwargs):
    t = template.loader.get_template(menu.template)

    viewable_nodes = [node for node in menu.values() if node.is_viewable_by(user)]
    if not viewable_nodes:
        return ''

    return t.render(template.Context({
        'menu': menu,
        'viewable_nodes': viewable_nodes,
        'user': user,
        'max_depth': max_depth,
    }))

@register.simple_tag(takes_context=True)
def render_node(context, **kwargs):
    node = kwargs.get('node', context.get('node'))
    if not node:
        raise ValueError('Missing node argument')

    user = kwargs.get('user', context.get('user', getattr(context.get('request', object()), 'user', None)))
    if not user:
        raise ValueError('missing user parameter')

    if not node.is_viewable_by(user):
        return ''

    max_depth = kwargs.get('max_depth', context.get('max_depth', 999))
    start_depth = kwargs.get('start_depth', context.get('start_depth', node.depth))
    current_depth = kwargs.get('current_depth', context.get('current_depth', node.depth - start_depth))

    viewable_children = []
    if current_depth + 1 <= max_depth:
        for child in node.children:
            if child.is_viewable_by(user):
                viewable_children.append(child)

    t = template.loader.get_template(node.template)

    return t.render(template.Context({
        'node': node,
        'viewable_children': viewable_children,
        'user': user,
        'max_depth': max_depth,
        'current_depth': current_depth,
        'start_depth': start_depth,
    }))

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
