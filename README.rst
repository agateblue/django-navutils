
Django-navutils is a lightweight package for handling menu and breadcrumbs inside
your django project.

Features:

- No database calls
- Highly customizable
- User targeting in menu, so you can display a menu node to users that match a specific criteria (authenticated, anonymous, staff member, or any custom check)
- Translatable

Requirements
============

- Python >= 2.7 or >= 3.3
- Django >= 1.7

The menu system may be integrated in any project, but the breadcrumbs part requires
that you use class-based views.

Install
=======

Package is available on pip and can be installed via ``pip install django-navutils``.

You'll also have to add ``navutils`` to your ``settings.INSTALLED_APPS``

Also add the following to ``settings.CONTEXT_PROCESSORS``::

    CONTEXT_PROCESSORS = (
        # ...
        'navutils.context_processors.menus',
    )

Usage
=====

Menus
*****

Navutils represents menus using ``Menu`` and ``Node`` instances, each menu being a collection of
node instances representing a menu link. Nodes may have children, which are also ``Node`` instances.

Let's see a minimal example.

``yourapp/menu.py``::

    from navutils import menu

    main_menu = menu.Menu('main')
    menu.register(main_menu)

    # will be shown to everybody
    blog = menu.Node(id='blog', label='Blog', pattern_name='blog:index')
    main_menu.register(blog)

    # nodes created with a pattern_name argument will use django reverse
    assert blog.get_url() == '/blog'

    # if you want to disable reversion, use the url argument
    django = menu.Node(id='django', label='Django project', url='http://djangoproject.com', link_attrs={'target': '_blank'})

    # Each node instance can accept an arbitrary number of children
    blog.children.add(menu.Node(id='last_entries', label='Last entries', pattern_name='blog:last_entries'))
    blog.children.add(menu.Node(id='archives', label='Archives', pattern_name='blog:archives'))

    # you can also make a link to any arbitrary URL
    django = menu.Node(id='django', label='Django project', url='http://djangoproject.com', link_attrs={'target': '_blank'})
    main_menu.register(django)

    # will be shown to anonymous users only
    login = menu.AnonymousNode(id='login', label='Login', pattern_name='accounts_login', link_attrs={'class': 'big-button'})
    main_menu.register(login)

    # will be shown to authenticated users only
    logout = menu.AuthenticatedNode(id='logout', label='Logout', pattern_name='accounts_logout')
    main_menu.register(login)


``yourapp/templates/index.html``::

    {% load navutils_tags %}
    {% render_menu menus.main user=request.user %}

For an anonymous user, this would input something like::

    <nav class="main-menu">
        <ul>
            <li class="has-children menu-item">
                <a href="/blog">Blog<a>
                <ul class="sub-menu">
                    <li class="menu-item">
                        <a href="/blog/latest">Latest entries</a>
                    </li>
                    <li class="menu-item">
                        <a href="/blog/archives">Archives</a>
                    </li>
                </ul>
            </li>
            <li class="menu-item">
                <a href="http://djangoproject.com" target="_blank">Django project</a>
            </li>
            <li class="menu-item">
                <a href="/login" class="big-button">Login</a>
            </li>
        </ul>
    </nav>


You can also directly set children nodes on parent instanciation with the ``children`` argument::

    user = menu.Node(
        id='user',
        label='Greetings',
        pattern_name='user:dashboard',
        children=[
            menu.Node(id='logout', label='Logout', pattern_name='user:logout'),

            # you can nest children indefinitely
            menu.Node(
                id='settings',
                label='Settings',
                pattern_name='user:settings',
                children = [
                    menu.Node(id='newsletter', label='Newsletter', pattern_name='user:settings:newsletter')
                ],
            ),
        ]
    )

Nodes can be customized in many ways::

    heavily_customized_node = menu.Node(
        'customized',
        'My custom menu',
        url='#',

        # a custom CSS class that will be applied to the node on rendering
        css_class='custom-class',

        # the <a> title attribute
        title='click me!',

        # a path to a custom template for rendering the node
        template='myapp/menu/mynode.html',

        # a dict of attributes that will be applied as HTML attributes on the <li>
        attrs = {'style': 'background-color: white;'}

        # a dict of attributes that will be applied as HTML attributes on the <a>
        link_attrs = {'target': '_blank', 'data-something': 'fancy-stuff'}
    )

If it's not enough, you can also override the default templates:

- ``navutils/menu.html`` : the menu wrapper that loop through the nodes
- ``navutils/node.html`` : called for displaying each node instance

Breadcrumbs
***********

Breadcrumbs are set up into views, and therefore can only be used with class-based views.

First of all, you'll probably want to define a base mixin for all your views::

    from navutils import BreadcrumbsMixin, Breadcrumb

    class BaseMixin(BreadcrumbsMixin):
        def get_breadcrumbs(self):
            breadcrumbs = super(BaseMixin, self).get_breadcrumbs()
            breadcrumbs.append(Breadcrumb('Home', url='/'))
            return breadcrumbs

Then, you can inherit from this view everywhere::

    # breadcrumbs = Home > Blog
    class BlogView(BaseMixin):
        title = 'Blog'


    # breadcrumbs = Home > Logout
    class LogoutView(BaseMixin):
        title = 'Logout'


By default, the last element of the breadcrumb is deduced from the ``title`` attribute of the view.
However, for a complex hierarchy, you are free to override the ``get_breadcrumbs`` method::

    # you can trigger url reversing via pattern_name, as for menu nodes
    class BlogMixin(BaseMixin)
        def get_breadcrumbs(self):
            breadcrumbs = super(BlogMixin, self).get_breadcrumbs()
            breadcrumbs.append(Breadcrumb('Blog', pattern_name='blog:index'))
            return breadcrumbs


    # breadcrumbs = Home > Blog > Last entries
    class BlogIndex(BlogMixin):
        title = 'Last entries'


    # for dynamic titles, just override the get_title method
    # breadcrumbs = Home > Blog > My category name
    class CategoryDetail(BlogMixin, DetailView):

        model = Category

        def get_title(self):
            # assuming your Category model has a title field
            return self.object.title


The last step is to render the breadcrumbs in your template. The provided mixin takes
care with passing data in the context, so all you need is::

    {% load navutils_tags %}

    {% render_breadcrumbs breadcrumbs %}

The breadcrumbs part of navutils is bundled with two templates, feel free to override them:

- ``navutils/breadcrumbs.html``: the breadcrumbs wrapper
- ``navutils/crumb.html``: used to render each crumb

That's it !
