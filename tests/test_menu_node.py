from django.test import LiveServerTestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from navutils import menu

User = get_user_model()


class BaseTestCase(LiveServerTestCase):
    def setUp(self):
        self.user = User(username='user')
        self.user.set_password('test')
        self.user.save()
        self.anonymous_user = AnonymousUser()

        self.admin = User(username='admin', is_superuser=True)
        self.admin.save()

        self.staff_member = User(username='staff', is_staff=True)
        self.staff_member.save()



class NodeTest(BaseTestCase):

    def test_menu_node_allows_arbitrary_url(self):
        node = menu.Node('Test', url='http://test.com')

        self.assertEqual(node.get_url(), 'http://test.com')

    def test_menu_node_allows_django_route(self):
        node = menu.Node('Test', route='index')

        self.assertEqual(node.get_url(), '/')

    def test_menu_node_allows_django_route_with_kwargs(self):
        node = menu.Node('Test', route='category', reverse_kwargs=['slug'])

        self.assertEqual(node.get_url(slug='test'), '/category/test')

    def test_children_keep_reference_to_parent(self):
        child = menu.Node('Child', url='http://test.com/child')
        parent = menu.Node('Test', url='http://test.com', children=[child])

        self.assertEqual(child.parent, parent)

    def test_node_depth(self):
        subchild = menu.Node('SubChild', url='http://test.com/subchild')
        child = menu.Node('Child', url='http://test.com/child', children=[subchild])
        parent = menu.Node('Test', url='http://test.com', children=[child])

        self.assertEqual(parent.depth, 0)
        self.assertEqual(child.depth, 1)
        self.assertEqual(subchild.depth, 2)


    def test_menu_node_sort_children_by_weight(self):
        child1 = menu.Node('Child1', weight=3, url='http://test.com/child1')
        child2 = menu.Node('Child2', weight=1, url='http://test.com/child2')
        child3 = menu.Node('Child3', weight=2, url='http://test.com/child3')

        parent = menu.Node(
            'Test',
            url='http://test.com',
            children=[
                child1,
                child2,
                child3,
            ]
        )

        self.assertEqual(parent.children, [child1, child3, child2])

        # we add another child, order should be updated
        child4 = menu.Node('Child4', weight=999, url='http://test.com/child4')
        parent.add(child4)

        self.assertEqual(parent.children, [child4, child1, child3, child2])

    def test_menu_node_is_viewable_by_anobody(self):
        node = menu.Node('Test', url='http://test.com')

        self.assertTrue(node.is_viewable_by(self.user))


class AnonymousNodeTest(BaseTestCase):

    def test_is_viewable_by_anonymous_user(self):
        node = menu.AnonymousNode('Test', url='http://test.com')

        self.assertTrue(node.is_viewable_by(self.anonymous_user))
        self.assertFalse(node.is_viewable_by(self.user))


class AuthenticatedNodeTest(BaseTestCase):

    def test_is_viewable_by_authenticated_user(self):
        node = menu.AuthenticatedNode('Test', url='http://test.com')

        self.assertFalse(node.is_viewable_by(self.anonymous_user))
        self.assertTrue(node.is_viewable_by(self.user))


class StaffNodeTest(BaseTestCase):

    def test_is_viewable_by_staff_members_or_admin(self):
        node = menu.StaffNode('Test', url='http://test.com')

        self.assertTrue(node.is_viewable_by(self.staff_member))
        self.assertTrue(node.is_viewable_by(self.admin))
        self.assertFalse(node.is_viewable_by(self.user))
        self.assertFalse(node.is_viewable_by(self.anonymous_user))
