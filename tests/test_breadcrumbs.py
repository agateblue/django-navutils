from django.test import LiveServerTestCase

from navutils import Breadcrumb


class BreadCrumbTest(LiveServerTestCase):
    def test_breadcrumb_reverse(self):
        crumb = Breadcrumb(label='Test', pattern_name='index')

        self.assertEqual(crumb.get_url(), '/')
