from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser, Permission
from django.test.client import RequestFactory

from navutils import menu
from navutils.templatetags import navutils_tags

User = get_user_model()


class BaseTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.user = User(username='user')
        self.user.set_password('test')
        self.user.save()
        self.anonymous_user = AnonymousUser()

        self.admin = User(username='admin', is_superuser=True)
        self.admin.save()

        self.staff_member = User(username='staff', is_staff=True)
        self.staff_member.save()



class MenuTest(BaseTestCase):
    def test_menu_can_register_nodes(self):
        main_menu = menu.Menu('main')
        node = menu.Node('test', 'Test', url='http://test.com')
        main_menu.register(node)

        self.assertEqual(main_menu['test'], node)


class NodeTest(BaseTestCase):

    def test_menu_node_allows_arbitrary_url(self):
        node = menu.Node('test', 'Test', url='http://test.com')

        self.assertEqual(node.get_url(), 'http://test.com')

    def test_menu_node_allows_django_pattern_name(self):
        node = menu.Node('test', 'Test', pattern_name='index')

        self.assertEqual(node.get_url(), '/')


    # def test_menu_node_allows_django_pattern_name_with_kwargs(self):
    #     node = menu.Node('test', 'Test', pattern_name='category', reverse_kwargs=['slug'])
    #
    #     self.assertEqual(node.get_url(slug='test'), '/blog/category/test')

    def test_children_keep_reference_to_parent(self):
        child = menu.Node('c', 'Child', url='http://test.com/child')
        parent = menu.Node('test', 'Test', url='http://test.com', children=[child])

        self.assertEqual(child.parent, parent)

    def test_node_depth(self):
        subchild = menu.Node('sc', 'SubChild', url='http://test.com/subchild')
        child = menu.Node('c', 'Child', url='http://test.com/child', children=[subchild])
        parent = menu.Node('test', 'Test', url='http://test.com', children=[child])

        self.assertEqual(parent.depth, 0)
        self.assertEqual(child.depth, 1)
        self.assertEqual(subchild.depth, 2)


    def test_menu_node_sort_children_by_weight(self):
        child1 = menu.Node('c1', 'Child1', weight=3, url='http://test.com/child1')
        child2 = menu.Node('c2', 'Child2', weight=1, url='http://test.com/child2')
        child3 = menu.Node('c3', 'Child3', weight=2, url='http://test.com/child3')

        children = [child1, child2, child3]
        parent = menu.Node(
            'test',
            'Test',
            url='http://test.com',
            children=children
        )

        self.assertEqual(parent.children, [child1, child3, child2])
        # we add another child, order should be updated
        child4 = menu.Node('c4', 'Child4', weight=999, url='http://test.com/child4')
        parent.add(child4)

        self.assertEqual(parent.children, [child4, child1, child3, child2])

    def test_children_accept_a_callable(self):

        def generate_children():
            return [menu.Node(i, i, url='#') for i in range(5)]

        parent = menu.Node(
            'test',
            'Test',
            url='http://test.com',
            children=generate_children
        )
        for i in range(5):
            self.assertEqual(parent.children[i].id, i)

    def test_menu_node_is_viewable_by_anobody(self):
        node = menu.Node('test', 'Test', url='http://test.com')

        self.assertTrue(node.is_viewable_by(self.user))


    def test_node_id_is_built_from_menu_and_parent(self):
        subchild = menu.Node('sc', 'SubChild', url='http://test.com/subchild')
        child = menu.Node('c', 'Child', url='http://test.com/child', children=[subchild])
        parent = menu.Node('test', 'Test', url='http://test.com', children=[child])


        self.assertEqual(parent.id, 'test')
        self.assertEqual(child.id, 'test:c')
        self.assertEqual(subchild.id, 'test:c:sc')

class AnonymousNodeTest(BaseTestCase):

    def test_is_viewable_by_anonymous_user(self):
        node = menu.AnonymousNode('test', 'Test', url='http://test.com')

        self.assertTrue(node.is_viewable_by(self.anonymous_user))
        self.assertFalse(node.is_viewable_by(self.user))


class AuthenticatedNodeTest(BaseTestCase):

    def test_is_viewable_by_authenticated_user(self):
        node = menu.AuthenticatedNode('test', 'Test', url='http://test.com')

        self.assertFalse(node.is_viewable_by(self.anonymous_user))
        self.assertTrue(node.is_viewable_by(self.user))


class StaffNodeTest(BaseTestCase):

    def test_is_viewable_by_staff_members_or_admin(self):
        node = menu.StaffNode('test', 'Test', url='http://test.com')

        self.assertTrue(node.is_viewable_by(self.staff_member))
        self.assertTrue(node.is_viewable_by(self.admin))
        self.assertFalse(node.is_viewable_by(self.user))
        self.assertFalse(node.is_viewable_by(self.anonymous_user))


class PermissionNodeTest(BaseTestCase):

    def test_is_viewable_by_user_with_required_permission(self):

        node = menu.PermissionNode('test', 'Test', url='http://test.com', permission='test_app.foo')

        self.assertTrue(node.is_viewable_by(self.admin))
        self.assertFalse(node.is_viewable_by(self.anonymous_user))
        self.assertFalse(node.is_viewable_by(self.user))

        permission = Permission.objects.get(codename='foo')
        self.user.user_permissions.add(permission)
        self.user = User.objects.get(pk=self.user.pk)

        self.assertTrue(node.is_viewable_by(self.user))


class AllPermissionsNodeTest(BaseTestCase):

    def test_is_viewable_by_user_with_required_permissions(self):

        node = menu.AllPermissionsNode('test', 'Test', url='http://test.com', permissions=['test_app.foo', 'test_app.bar'])

        self.assertTrue(node.is_viewable_by(self.admin))
        self.assertFalse(node.is_viewable_by(self.anonymous_user))
        self.assertFalse(node.is_viewable_by(self.user))

        permission = Permission.objects.get(codename='foo')
        self.user.user_permissions.add(permission)
        self.user = User.objects.get(pk=self.user.pk)

        self.assertFalse(node.is_viewable_by(self.user))

        permission = Permission.objects.get(codename='bar')
        self.user.user_permissions.add(permission)
        self.user = User.objects.get(pk=self.user.pk)

        self.assertTrue(node.is_viewable_by(self.user))


class AnyPermissionsNodeTest(BaseTestCase):

    def test_is_viewable_by_user_with_any_required_permissions(self):

        node = menu.AnyPermissionsNode('test', 'Test', url='http://test.com', permissions=['test_app.foo', 'test_app.bar'])

        self.assertTrue(node.is_viewable_by(self.admin))
        self.assertFalse(node.is_viewable_by(self.anonymous_user))
        self.assertFalse(node.is_viewable_by(self.user))

        permission = Permission.objects.get(codename='foo')
        self.user.user_permissions.add(permission)
        self.user = User.objects.get(pk=self.user.pk)

        self.assertTrue(node.is_viewable_by(self.user))

        self.user.user_permissions.remove(permission)

        permission = Permission.objects.get(codename='bar')
        self.user.user_permissions.add(permission)
        self.user = User.objects.get(pk=self.user.pk)

        self.assertTrue(node.is_viewable_by(self.user))


class PassTestNode(BaseTestCase):

    def test_is_viewable_by_user_with_any_required_permissions(self):
        test = lambda user, context: 'chuck' in user.username

        node = menu.PassTestNode('test', 'Test', url='http://test.com', test=test)

        self.assertFalse(node.is_viewable_by(self.admin))
        self.assertFalse(node.is_viewable_by(self.user))

        self.user.username = 'chucknorris'

        self.assertTrue(node.is_viewable_by(self.user))



class RenderNodeTest(BaseTestCase):

    def test_render_node_template_tag(self):
        node = menu.Node('test', 'Test', url='http://test.com')

        output = navutils_tags.render_node({}, node=node, user=self.user)
        self.assertHTMLEqual(
            output,
            '<li class="menu-item"><a href="http://test.com">Test</a></li>')

    def test_render_node_template_tag_with_extra_context(self):
        node = menu.Node('test', 'Test', url='http://test.com', template='test_app/test_node.html',
                         context={'foo': 'bar'})

        output = navutils_tags.render_node({}, node=node, user=self.user)
        self.assertHTMLEqual(
            output,
            '<li class="menu-item"><a href="http://test.com">Test bar</a></li>')


    def test_render_node_template_tagwith_current(self):
        node = menu.Node('test', 'Test', url='http://test.com')

        output = navutils_tags.render_node({'current_menu_item':'test'}, node=node, user=self.user)
        self.assertHTMLEqual(
            output,
            '<li class="menu-item current"><a href="http://test.com">Test</a></li>')


    def test_render_node_template_tag_with_link_attrs(self):
        attrs = {'target': '_blank', 'title': 'Click me !'}
        node = menu.Node('test', 'Test', url='http://test.com', link_attrs=attrs)

        output = navutils_tags.render_node({}, node=node, user=self.user)
        self.assertHTMLEqual(
            output,
            """<li class="menu-item">
                <a href="http://test.com" target="_blank" title="Click me !">Test</a>
            </li>""")

    def test_render_node_template_tag_with_node_attrs(self):
        attrs = {'id': 'important'}
        node = menu.Node('test', 'Test', url='http://test.com', attrs=attrs)

        output = navutils_tags.render_node({}, node=node, user=self.user)
        self.assertHTMLEqual(
            output,
            """<li class="menu-item" id="important">
                <a href="http://test.com">Test</a>
            </li>""")

    def test_render_node_template_tag_with_children(self):
        child1 = menu.Node('c1', 'c1', url='c1')
        child2 = menu.Node('c2', 'c2', url='c2')
        child3 = menu.Node('c3', 'c3', url='c3')

        node = menu.Node(
            'test',
            'Test',
            url='http://test.com',
            children=[
                child1,
                child2,
                child3,
            ]
        )

        output = navutils_tags.render_node({}, node=node, user=self.user)

        self.assertHTMLEqual(
            output,
            """
            <li class="menu-item has-children has-dropdown">
                <a href="http://test.com">Test</a>
                <ul class="sub-menu dropdown">
                    <li class="menu-item"><a href="c1">c1</a></li>
                    <li class="menu-item"><a href="c2">c2</a></li>
                    <li class="menu-item"><a href="c3">c3</a></li>
                </ul>
            </li>
            """)

    def test_render_node_template_tag_with_children_and_current(self):
        child1 = menu.Node('c1', 'c1', url='c1')
        child2 = menu.Node('c2', 'c2', url='c2')
        child3 = menu.Node('c3', 'c3', url='c3')

        node = menu.Node(
            'test',
            'Test',
            url='http://test.com',
            children=[
                child1,
                child2,
                child3,
            ]
        )

        output = navutils_tags.render_node({'current_menu_item':'test:c3'}, node=node, user=self.user)

        self.assertHTMLEqual(
            output,
            """
            <li class="menu-item has-children has-current has-dropdown">
                <a href="http://test.com">Test</a>
                <ul class="sub-menu dropdown">
                    <li class="menu-item"><a href="c1">c1</a></li>
                    <li class="menu-item"><a href="c2">c2</a></li>
                    <li class="menu-item current"><a href="c3">c3</a></li>
                </ul>
            </li>
            """)

    def test_render_node_template_tag_with_children_and_depth(self):
        subchild = menu.Node('s1', 's1', url='s1')
        child1 = menu.Node('c1', 'c1', url='c1', children=[subchild])
        child2 = menu.Node('c2', 'c2', url='c2')
        child3 = menu.Node('c3', 'c3', url='c3')

        node = menu.Node(
            'test',
            'Test',
            url='http://test.com',
            children=[
                child1,
                child2,
                child3,
            ]
        )

        output = navutils_tags.render_node({}, node=node, user=self.user, max_depth=1)

        self.assertHTMLEqual(
            output,
            """
            <li class="menu-item has-children has-dropdown">
                <a href="http://test.com">Test</a>
                <ul class="sub-menu dropdown">
                    <li class="menu-item"><a href="c1">c1</a></li>
                    <li class="menu-item"><a href="c2">c2</a></li>
                    <li class="menu-item"><a href="c3">c3</a></li>
                </ul>
            </li>
            """)

        output = navutils_tags.render_node({}, node=node, user=self.user, max_depth=0)

        self.assertHTMLEqual(
            output,
            """
            <li class="menu-item">
                <a href="http://test.com">Test</a>
            </li>
            """)


class MenuMixinTest(BaseTestCase):

    def test_set_current_menu_item_in_context(self):
        response = self.client.get('/')
        self.assertEqual(response.context['current_menu_item'], 'test:index')


class RenderMenuTest(BaseTestCase):

    def test_template_tag(self):
        main_menu = menu.Menu('main')
        node = menu.Node('test', 'Test', url='http://test.com')
        main_menu.register(node)

        output = navutils_tags.render_menu({}, menu=main_menu, user=self.user)

        self.assertHTMLEqual(
            output,
            """
            <ul class="main-menu">
                <li class="menu-item"><a href="http://test.com">Test</a></li>
            </ul>
            """)
