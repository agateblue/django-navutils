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



class NodeTest(BaseTestCase):

    def test_menu_node_allows_arbitrary_url(self):
        node = menu.Node('Example', url='http://example.com')
        self.assertEqual(node.get_url(), 'http://example.com')

    def test_menu_node_allows_django_route(self):
        node = menu.Node('Example', route='index')
        self.assertEqual(node.get_url(), '/')

    def test_menu_node_allows_django_route_with_kwargs(self):
        node = menu.Node('Example', route='category', reverse_kwargs=['slug'])
        self.assertEqual(node.get_url(slug='test'), '/category/test')

    def test_menu_node_sort_children_by_weight(self):
        child1 = menu.Node('Child1', weight=3, url='http://example.com/child1')
        child2 = menu.Node('Child2', weight=1, url='http://example.com/child2')
        child3 = menu.Node('Child3', weight=2, url='http://example.com/child3')

        parent = menu.Node(
            'Example',
            url='http://example.com',
            children=[
                child1,
                child2,
                child3,
            ]
        )

        self.assertEqual(parent.children, [child1, child3, child2])

        # we add another child, order should be updated
        child4 = menu.Node('Child4', weight=999, url='http://example.com/child4')
        parent.add(child4)

        self.assertEqual(parent.children, [child4, child1, child3, child2])

    def test_menu_node_is_viewable_by_anobody(self):
        node = menu.Node('Example', url='http://example.com')
        self.assertTrue(node.is_viewable_by(self.user))


class AnonymousNodeTest(BaseTestCase):

    def test_is_viewable_by_anonymous_user(self):
        node = menu.AnonymousNode('Example', url='http://example.com')

        self.assertTrue(node.is_viewable_by(self.anonymous_user))
        self.assertFalse(node.is_viewable_by(self.user))
