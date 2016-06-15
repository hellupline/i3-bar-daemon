from cached_property import cached_property_with_ttl
import i3_status_line.base as base

THERMAL_FILE = '/sys/class/thermal/thermal_zone{}/temp'


class Widget(base.WidgetMixin):
    name = 'cpu-temperature'

    def __init__(self, theme, reading=0):
        self.reading = reading
        super().__init__(theme)

    def render(self):
        temperature = self.cpu_temperature()
        return self._render_widget(
            color=self.get_color(temperature),
            icon='🌡', text='{}°C'.format(temperature),
        )

    def get_color(self, temperature):
        if temperature < 45:
            return self._color('info')
        elif temperature < 55:
            return self._color('warning')
        return self._color('danger')

    def cpu_temperature(self):
        with open(THERMAL_FILE.format(self.reading)) as f:
            return int(f.read().strip()) // 1000

    @cached_property_with_ttl(ttl=5)
    def state(self):
        return self.render()


if __name__ == '__main__':
    base.debug(Widget)
