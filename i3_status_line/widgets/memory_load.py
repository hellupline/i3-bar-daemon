import psutil

from cached_property import cached_property_with_ttl
import i3_status_line.base as base


class Widget(base.WidgetMixin):
    name = 'memory-load'

    def render(self):
        load = psutil.virtual_memory().percent
        return self._render_widget(
            color=self.get_color(load),
            icon='', text='{:.2f}%'.format(load),
            icon_only=not self.show_text,
        )

    def get_color(self, load):
        if load > 75:
            return self._color('danger')
        elif load > 50:
            return self._color('warning')
        return self._color('info')

    @cached_property_with_ttl(ttl=5)
    def state(self):
        return self.render()


if __name__ == '__main__':
    base.debug(Widget)
