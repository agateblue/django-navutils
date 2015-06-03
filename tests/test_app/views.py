from django.views.generic import TemplateView

from navutils import Breadcrumb, BreadcrumbsMixin, MenuMixin


def blank():
    return


class BaseMixin(BreadcrumbsMixin, MenuMixin, TemplateView):

    def get_breadcrumbs(self):
        breadcrumbs = super(BaseMixin, self).get_breadcrumbs()
        breadcrumbs.append(Breadcrumb('Home', url='/'))
        return breadcrumbs


class Index(BaseMixin):
    current_menu_item = 'test:index'


class BlogMixin(BaseMixin):
    def get_breadcrumbs(self):
        breadcrumbs = super(BlogMixin, self).get_breadcrumbs()
        breadcrumbs.append(Breadcrumb('Blog', url='/blog'))
        return breadcrumbs

class CategoryMixin(BlogMixin):

    def get_title(self):
        return self.kwargs['slug'].title()

    def get_current_url(self):
        return '/blog/category/{0}'.format(self.kwargs['slug'])
