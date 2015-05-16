from django.test import TestCase
from navutils.menu import MenuNode

class MenuNodeTest(TestCase):

    def test_menu_node_allows_arbitrary_url(self):
        menu_node = MenuNode('Example', url='http://example.com')
        self.assertEqual(menu_node.get_url(), 'http://example.com')

    def test_menu_node_allows_django_routes(self):
        menu_node = MenuNode('Example', route='index')
        self.assertEqual(menu_node.get_url(), '/')
