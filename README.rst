
Django-navutils is a lightweight package for handling menu and breadcrumbs inside
your django project.

Features:

- No database calls
- Highly customizable
- User targeting in menu, so you can display a menu node to users that match a specific
criteria (authenticated, anonymous, staff member, or any custom check)
- Translatable

Requirements
============

The project is tested under python 2.7 and 3.4, along with django 1.7 and 1.8.

The menu system may be integrated in any project, but the breadcrumbs part requires
that you use class-based views.

Install
=======

Package is available on pip and can be installed via ``pip install django-navutils``.

You'll also have to add ``navutils`` to your ``settings.INSTALLED_APPS``

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

    # Let's add some children
    blog.children.add(menu.Node(id='last_entries', label='Last entries'), pattern_name='blog:last_entries')
    blog.children.add(menu.Node(id='archives', label='Archives'), pattern_name='blog:archives')

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
    {% render_menu 'main' %}

For an anonymous user, this would input something like::


    <nav class="main">
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


You can also add children nodes upon parent instanciation via the ``children`` argument::

    user = menu.Node(
        id='user',
        label='Greetings',
        pattern_name='user:dashboard',
        children=[
            menu.Node(id='logout', label='Logout', pattern_name='user:logout'),

            # you can nest chldren indefinitely
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

    )
