

class MenuMixin(object):
    current_menu_item = None

    def get_current_menu_item(self):
        return self.current_menu_item

    def get_context_data(self, **kwargs):
        context = super(MenuMixin, self).get_context_data(**kwargs)
        context['current_menu_item'] = self.get_current_menu_item()
        return context
