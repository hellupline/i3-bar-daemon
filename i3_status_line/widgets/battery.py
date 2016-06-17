from cached_property import cached_property_with_ttl
import i3_status_line.base as base

BAT_FILE = '/sys/class/power_supply/{}/{}'


class Widget(base.WidgetMixin):
    name = 'battery-monitor'

    def __init__(self, theme, battery='BAT0'):
        self.instance = self.battery = battery
        super().__init__(theme)

    def render(self):
        capacity = self.battery_capacity()
        status = self.battery_status()
        return self._render_widget(
            color=self.get_color(capacity),
            icon=self.get_icon(capacity, status),
            text='{}%'.format(capacity),
        )

    def get_color(self, capacity):
        if capacity < 20:
            return self._color('danger')
        elif capacity < 60:
            return self._color('warning')
        elif capacity < 80:
            return self._color('info')
        return self._color('text')

    def get_icon(self, capacity, status):
        if status != 'Discharging':
            return ''
        if capacity < 20:
            return ''
        elif capacity < 40:
            return ''
        elif capacity < 60:
            return ''
        elif capacity < 80:
            return ''
        return ''

    def battery_capacity(self):
        with open(BAT_FILE.format(self.battery, 'capacity')) as f:
            return int(f.read().strip())

    def battery_status(self):
        with open(BAT_FILE.format(self.battery, 'status')) as f:
            return f.read().strip()

    @cached_property_with_ttl(ttl=5)
    def state(self):
        return self.render()


if __name__ == '__main__':
    base.debug(Widget)
