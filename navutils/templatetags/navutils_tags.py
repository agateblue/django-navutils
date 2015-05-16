from django import template

register = template.Library()


@register.simple_tag
def render_node(node, user):
    
    t = template.loader.get_template(node.template)


    return t.render(template.Context({
        'node': node,
    }))
