from cached_property import cached_property_with_ttl
from ..base import WidgetMixin, debug

THERMAL_FILE = '/sys/class/thermal/thermal_zone{}/temp'


class Widget(WidgetMixin):
    icon = '🌡'
    fmt = '{}°C'.format
    name = 'cpu-temperature'

    def __init__(self, config, reading=0, alert=55):
        self.reading = reading
        self.alert = alert
        super().__init__(config)

    @cached_property_with_ttl(ttl=5)
    def state(self):
        temperature = self.cpu_temperature()
        if temperature < self.alert and self.show():
            return ()
        return (
            self.make_icon({'text': self.icon}),
            self.make_text({
                'color': self.get_color(temperature),
                'text': self.fmt(temperature),
            }),
            self.make_separator(),
        )

    def get_color(self, temperature):
        if temperature < 45:
            return self.pallete('info')
        elif temperature < 55:
            return self.pallete('warning')
        return self.pallete('danger')

    def cpu_temperature(self):
        with open(THERMAL_FILE.format(self.reading)) as f:
            return int(f.read().strip()) // 1000


if __name__ == '__main__':
    debug(Widget)
