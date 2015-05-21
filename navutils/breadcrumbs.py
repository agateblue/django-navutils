from django.core.urlresolvers import reverse


class Breadcrumb(object):
    def __init__(self, label, pattern_name=None, url=None, title=None, css_class=None,
                 reverse_kwargs=[], **kwargs):
        if pattern_name and url:
            raise ValueError('Breadcrumb accepts either a url or a pattern_name arg, but not both')
        if not pattern_name and not url:
            raise ValueError('Breadcrumb needs either a url or a pattern_name arg')

        self.pattern_name = pattern_name
        self.url = url
        self.label = label
        self.css_class = css_class
        self.reverse_kwargs = reverse_kwargs

    def get_url(self, **kwargs):
        if self.pattern_name:
            expected_kwargs = {
                key: value for key, value in kwargs.items()
                if key in self.reverse_kwargs
            }
            return reverse(self.pattern_name, kwargs=expected_kwargs)
        return self.url


class BreadcrumbsMixin(object):

    title = ''
    current_url = None

    def get_title(self):
        return self.title

    def get_current_url(self):
        return self.current_url

    def get_context_data(self, **kwargs):
        context = super(BreadcrumbsMixin, self).get_context_data(**kwargs)
        breadcrumbs = self.get_breadcrumbs()

        title = self.get_title()
        seo_title = title

        # auto bread-crumb from title
        if title:
            if breadcrumbs and breadcrumbs[-1].label != title:
                url = self.get_current_url() or '#'
                breadcrumbs.append(Breadcrumb(url=url, reverse=False, label=title))

        try:
            # append parent breadcrumb title for better SEO
            if seo_title and breadcrumbs[-2] != breadcrumbs[0] and breadcrumbs[-2].label:
                seo_title += ' - {0}'.format(breadcrumbs[-2].label)
        except IndexError:
            pass

        context['breadcrumbs'] = breadcrumbs
        context['title'] = title
        context['seo_title'] = seo_title

        return context

    def get_breadcrumbs(self):
        return []
