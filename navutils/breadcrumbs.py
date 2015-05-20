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
