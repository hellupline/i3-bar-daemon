import psutil

from cached_property import cached_property_with_ttl
import i3_status_line.base as base


class Widget(base.WidgetMixin):
    def render(self):
        load = psutil.virtual_memory().percent
        return self._render_widget(
            color=self._color('text'),
            icon='!', text='Hello World!',
        )

    @cached_property_with_ttl(ttl=5)
    def state(self):
        return self.render()


if __name__ == '__main__':
    base.debug(Widget)
