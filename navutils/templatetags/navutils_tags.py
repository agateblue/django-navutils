from django import template

register = template.Library()


@register.simple_tag
def render_menu(menu, user, max_depth=999, **kwargs):
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

@register.simple_tag
def render_node(node, user, max_depth=999, current_depth=None, start_depth=None):
    if not node.is_viewable_by(user):
        return ''
    start_depth = start_depth or node.depth
    current_depth = current_depth or node.depth - start_depth

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

@register.simple_tag
def render_crumb(crumb, **kwargs):

    t = template.loader.get_template('navutils/crumb.html')

    return t.render(template.Context({
        'crumb': crumb,
        'last': kwargs.get('last', False),
    }))

@register.simple_tag
def render_breadcrumbs(crumbs, **kwargs):

    t = template.loader.get_template('navutils/breadcrumbs.html')

    return t.render(template.Context({
        'crumbs': crumbs,
    }))
