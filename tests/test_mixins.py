from django.test import TestCase
from django.views.generic import TemplateView
from django.test.client import RequestFactory

from navutils import mixins
from navutils.templatetags import navutils_tags


class MixinsTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_title_mixin(self):

        class TitleView(mixins.TitleMixin, TemplateView):
            template_name = 'test_app/test.html'
            title = 'yolo'

        view = TitleView.as_view()
        response = view(self.factory.get('/'))

        self.assertEqual(response.context_data['title'], 'yolo')

    def test_dynamic_title_mixin(self):

        class TitleView(mixins.TitleMixin, TemplateView):
            template_name = 'test_app/test.html'
            def get_title(self):
                return self.__class__.__name__

        view = TitleView.as_view()
        response = view(self.factory.get('/'))

        self.assertEqual(response.context_data['title'], 'TitleView')

    def test_dynamic_description_mixin(self):

        class DescriptionView(mixins.DescriptionMixin, TemplateView):
            template_name = 'test_app/test.html'
            def get_description(self):
                return self.__class__.__name__

        view = DescriptionView.as_view()
        response = view(self.factory.get('/'))

        self.assertEqual(response.context_data['description'], 'DescriptionView')

    def test_description_mixin(self):

        class DescriptionView(mixins.DescriptionMixin, TemplateView):
            template_name = 'test_app/test.html'
            description = 'my meta description'

        view = DescriptionView.as_view()
        response = view(self.factory.get('/'))

        self.assertEqual(response.context_data['description'], 'my meta description')
