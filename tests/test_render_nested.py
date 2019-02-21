from django.test import TestCase
from django.template import Context

from navutils.templatetags import navutils_tags


class RenderNestedTest(TestCase):

    def test_render_nested_block(self):
        block = '{% filter lower %}This Will All Be Lower{% endfilter %}'

        output = navutils_tags.render_nested(Context({}), block)
        self.assertEqual(
            output,
            'this will all be lower')

    def test_render_nested_variable(self):
        block = '{{ value|join:" // " }}'

        output = navutils_tags.render_nested(Context({'value': [1, 2, 3]}), block)
        self.assertEqual(
            output,
            '1 // 2 // 3')
