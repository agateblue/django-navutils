from django.test import TestCase
from navutils.menu import MenuNode

class MenuNodeTest(TestCase):

    def test_menu_node_allows_arbitrary_url(self):
        menu_node = MenuNode('Example', url='http://example.com')
        self.assertEqual(menu_node.get_url(), 'http://example.com')

    def test_menu_node_allows_django_route(self):
        menu_node = MenuNode('Example', route='index')
        self.assertEqual(menu_node.get_url(), '/')

    def test_menu_node_allows_django_route_with_kwargs(self):
        menu_node = MenuNode('Example', route='category', reverse_kwargs=['slug'])
        self.assertEqual(menu_node.get_url(slug='test'), '/category/test')

    def test_menu_node_sort_children_by_weight(self):
        child1 = MenuNode('Child1', weight=3, url='http://example.com/child1')
        child2 = MenuNode('Child2', weight=1, url='http://example.com/child2')
        child3 = MenuNode('Child3', weight=2, url='http://example.com/child3')

        parent = MenuNode(
            'Example',
            url='http://example.com',
            children=[
                child1,
                child2,
                child3,
            ]
        )

        self.assertEqual(parent.children, [child1, child3, child2])

        child4 = MenuNode('Child4', weight=999, url='http://example.com/child4')
        parent.add(child4)

        self.assertEqual(parent.children, [child4, child1, child3, child2])
