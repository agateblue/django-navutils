
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

Navutils represents menus using `Menu` and `Node` instances, each menu being a collection of
node instances representing a menu link. Nodes may have children, which are also `Node` instances::

    from navutils import menu

    main_menu = menu.Menu('main')
    menu.register(main_menu)

    # will be shown to everybody
    blog = menu.Node(id='blog', label='Blog', pattern_name='blog:index')
    main_menu.register(blog)

    # will be shown to anonymous users only
    login = menu.AnonymousNode(id='login', label='Login', pattern_name='accounts_login')
    main_menu.register(login)

    # will be shown to authenticated users only
    logout = menu.AuthenticatedNode(id='logout', label='Logout', pattern_name='accounts_logout')
    main_menu.register(login)

    # you can also make a link to any arbitrary URL
    django = menu.Node(id='django', label='Django project', url='http://djangoproject.com')
    main_menu.register(django)
