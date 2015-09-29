


class TitleMixin(object):
    title = None

    def get_title(self):
        return self.title

    def get_context_data(self, **kwargs):
        context = super(TitleMixin, self).get_context_data(**kwargs)
        context['title'] = self.get_title()
        return context


class DescriptionMixin(object):
    description = None

    def get_description(self):
        return self.description

    def get_context_data(self, **kwargs):
        context = super(DescriptionMixin, self).get_context_data(**kwargs)
        context['description'] = self.get_description()
        return context
