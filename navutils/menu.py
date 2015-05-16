from django.core.urlresolvers import reverse

from persisting_theory import Registry


class Menu(Registry):
    look_into = 'menu'

    def prepare_name(self, data, name=None):
        return data.id

menu = Menu()


class Node(object):

    parent = None

    def __init__(self, id, label, route=None, url=None, weight=0,
                 template='navutils/menu/node.html', **kwargs):
        """
        :param str id: a unique identifier for further retrieval
        :param str label: a label for the node, that will be displayed in templates
        :param str route: the name of a django url, such as `myapp:index` to use
        as a link for the node. It will be automatically reversed.
        :param str url: a URL to use as a link for the node
        :param int weight: The importance of the node. Higher is more\
        important, default to ``0``.
        :param list reverse_kwargs: A list of strings that the route will\
        accept when reversing. Defaults to ``[]``
        :param list children: A list of children :py:class:`Node` instances\
        that will be considered as submenus of this instance.\
        Defaults to ``[]``.
        :param str css_class: a CSS class that will be applied to the node when
        rendering
        :param str title: a title to populate the html title attribute of the node
        :param str template: the template that will be used to render the node.\
        defaults to `navutils/menu/node.html`
        """
        if route and url:
            raise ValueError('MenuNode accepts either a url or a route arg, but not both')
        if not route and not url:
            raise ValueError('MenuNode needs either a url or a route arg')

        self.id = id
        self.route = route
        self.url = url
        self.label = label
        self.title = kwargs.get('title')
        self.weight = weight
        self.template = template
        self.css_class = kwargs.get('css_class')

        self.reverse_kwargs = kwargs.get('reverse_kwargs', [])

        self.children = []
        for node in kwargs.get('children', []):
            self.add(node)

    def get_url(self, **kwargs):
        """
        :param kwargs: a dictionary of values that will be used for reversing,\
        if the corresponding key is present in :py:attr:`self.reverse_kwargs\
        <Node.reverse_kwargs>`
        :return: The target URL of the node, after reversing (if needed)
        """
        if self.route:
            expected_kwargs = {
                key: value for key, value in kwargs.items()
                if key in self.reverse_kwargs
            }
            return reverse(self.route, kwargs=expected_kwargs)
        return self.url

    def add(self, node):
        """
        Add a new node to the instance children and sort them by weight.

        :param node: A node instance
        """
        node.parent = self
        self.children.append(node)
        self.children = sorted(
            self.children,
            key=lambda i: i.weight,
            reverse=True
        )

    def is_viewable_by(self, user):
        return True

    @property
    def depth(self):
        return 0 if not self.parent else self.parent.depth + 1


class AnonymousNode(Node):
    """Only viewable by anonymous users"""
    def is_viewable_by(self, user):
        return not user.is_authenticated()


class AuthenticatedNode(Node):
    """Only viewable by authenticated users"""
    def is_viewable_by(self, user):
        return user.is_authenticated()


class StaffNode(AuthenticatedNode):
    """Only viewable by staff members / admins"""

    def is_viewable_by(self, user):
        return user.is_staff or user.is_superuser
