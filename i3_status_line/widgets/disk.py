import psutil

from cached_property import cached_property_with_ttl
import i3_status_line.base as base


class Widget(base.WidgetMixin):
    name = 'disk'

    def __init__(self, theme, path='/'):
        self.instance = self.path = path
        super().__init__(theme)

    def render(self):
        free_space = self.free_space()
        return self._render_widget(
            color=self.get_color(free_space),
            icon='', text='{}G'.format(free_space),
        )

    def get_color(self, free_space):
        if free_space < 40:
            self._color('danger')
        return self._color('info')

    def free_space(self):
        return psutil.disk_usage(self.path).free // 1073741824  # 1024**3 (Gb)

    @cached_property_with_ttl(ttl=5)
    def state(self):
        return self.render()


if __name__ == '__main__':
    base.debug(Widget)
