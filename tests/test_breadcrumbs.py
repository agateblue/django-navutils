from django.test import TestCase

from navutils import Breadcrumb
from navutils.templatetags import navutils_tags


class BreadcrumbTest(TestCase):
    def test_breadcrumb_reverse(self):
        crumb = Breadcrumb(label='Test', pattern_name='index')

        self.assertEqual(crumb.get_url(), '/')

    def test_breadcrumb_url(self):
        crumb = Breadcrumb(label='Test', url='http://test.com')

        self.assertEqual(crumb.get_url(), 'http://test.com')

    def test_mixin_pass_context_data(self):
        response = self.client.get('/')

        self.assertEqual(response.context['breadcrumbs'][0].get_url(), '/' )
        self.assertEqual(response.context['breadcrumbs'][0].label, 'Home')

    def test_mixin_inherit_crumbs(self):
        response = self.client.get('/blog')

        self.assertEqual(response.context['breadcrumbs'][0].get_url(), '/' )
        self.assertEqual(response.context['breadcrumbs'][0].label, 'Home')

        self.assertEqual(response.context['breadcrumbs'][1].get_url(), '/blog' )
        self.assertEqual(response.context['breadcrumbs'][1].label, 'Blog')

        response = self.client.get('/blog/category/test')

        self.assertEqual(response.context['breadcrumbs'][0].get_url(), '/' )
        self.assertEqual(response.context['breadcrumbs'][0].label, 'Home')

        self.assertEqual(response.context['breadcrumbs'][1].get_url(), '/blog' )
        self.assertEqual(response.context['breadcrumbs'][1].label, 'Blog')

        self.assertEqual(response.context['breadcrumbs'][2].get_url(), '/blog/category/test' )
        self.assertEqual(response.context['breadcrumbs'][2].label, 'Test')


class RenderBreadcrumbTest(TestCase):

    def test_render_single_crumb(self):
        crumb = Breadcrumb(label='Test', pattern_name='index')

        output = navutils_tags.render_crumb({}, crumb)
        self.assertHTMLEqual(
            output,
            '<li class="crumb"><a href="/">Test</a></li>')

    def test_render_breadcrumbs(self):
        crumbs = []
        crumbs.append(Breadcrumb(label='Test1', pattern_name='index'))
        crumbs.append(Breadcrumb(label='Test2', url='http://test.com'))

        output = navutils_tags.render_breadcrumbs({}, crumbs)
        self.assertHTMLEqual(
            output,
            """
            <ul class="breadcrumbs">
                <li class="crumb"><a href="/">Test1</a></li>
                <li class="crumb current"><a href="http://test.com">Test2</a></li>
            </ul>
            """)
