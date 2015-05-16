from django.core.urlresolvers import reverse

class MenuNode(object):
    """
    Describe a menu element, and may be attached to an
    :py:class:`App <kii.app.core.App>` instance (via the :py:attr:`menu
    <kii.app.core.App.menu>` attribute) for automatic inclusion in templates.
    """

    def __init__(self, label, route=None, url=None, weight=0,
                 template='navutils/menu/node.html', **kwargs):
        """
        :param str route: Either a relative URL, absolute URL or a django URL\
        name, such as ``myapp:index``. Defaults to ``#``.
        :param bool reverse: Wether the given route should be reversed using\
        django's :py:func:`reverse` or returned 'as is'. Defaults to ``True``.
        :param int weight: Indicate the importance of the node. Higher is more\
        important, default to ``0``.
        :param function is_viewable_by: Used to determine if the node\
        should be shown to request user. Defaults to ``True``.
        :param list reverse_kwargs: A list of strings that the route will\
        accept when reversing. Defaults to ``[]``
        :param list children: A list of children :py:class:`MenuNode` instances\
        that will be considered as submenus of this instance.\
        Defaults to ``[]``.
        :param icon: TODO, seems useless.

        """
        if route and url:
            raise ValueError('MenuNode accepts either a url or a route arg, but not both')
        if not route and not url:
            raise ValueError('MenuNode needs either a url or a route arg')

        self.route = route
        self.url = url
        self.label = label
        self.title = kwargs.get('title')
        self.weight = weight
        self.template = template
        self.css_class = kwargs.get('css_class')

        self.reverse_kwargs = kwargs.get('reverse_kwargs', [])

        self.children = []
        for item in kwargs.get('children', []):
            self.add(item)

    def get_url(self, **kwargs):
        """
        :param kwargs: a dictionary of values that will be used for reversing,\
        if the corresponding key is present in :py:attr:`self.reverse_kwargs\
        <MenuNode.reverse_kwargs>`
        :return: The target URL of the node, after reversing (if needed)
        """
        if self.route:
            expected_kwargs = {
                key: value for key, value in kwargs.items()
                if key in self.reverse_kwargs
            }
            return reverse(self.route, kwargs=expected_kwargs)
        return self.url

    def add(self, item):
        """
        Add a new node to the instance children and sort them by weight.

        :param item: A menu node instance
        """
        self.children.append(item)
        self.children = sorted(
            self.children,
            key=lambda i: i.weight,
            reverse=True
        )

    def is_viewable_by(self, user):
        return True
