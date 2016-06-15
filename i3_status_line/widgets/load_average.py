import os

from cached_property import cached_property_with_ttl
import i3_status_line.base as base


class Widget(base.WidgetMixin):
    name = 'load-average'

    def render(self):
        one, five, fifteen = os.getloadavg()
        cpu_count = os.cpu_count()
        return self._render_widget(
            color=self.get_color(one, cpu_count),
            icon='☢', text='{:.2f}'.format(one),
        )

    def get_color(self, value, total_cpus):
        if value > total_cpus:
            return self._color('danger')
        return self._color('info')

    @cached_property_with_ttl(ttl=5)
    def state(self):
        return self.render()


if __name__ == '__main__':
    base.debug(Widget)
