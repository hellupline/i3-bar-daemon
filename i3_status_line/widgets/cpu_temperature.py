from cached_property import cached_property_with_ttl
from ..base import WidgetMixin, DEFAULT_THEME

THERMAL_FILE = '/sys/class/thermal/thermal_zone{}/temp'


class Widget(WidgetMixin):
    icon = '🌡'
    fmt = '{}°C'.format
    name = 'cpu-temperature'

    def __init__(self, config, core=0, alert=55):
        self.alert = alert
        self.core = core
        super().__init__(config)
        self.color, = self.pallete(['danger'])

    @cached_property_with_ttl(ttl=5)
    def state(self):
        temp = self.cpu_temperature()
        if temp < self.alert and self.config['hide_on_zero']:
            return ()
        return (
            self.make_icon({'text': self.icon}),
            self.make_text({
                'color': self.color,
                'text': self.fmt(temp),
            }),
            self.make_separator(),
        )

    def cpu_temperature(self):
        with open(THERMAL_FILE.format(self.core)) as f:
            return int(f.read().strip()) // 1000


if __name__ == '__main__':
    print(Widget({**DEFAULT_THEME, 'hide_on_zero': False}).state)
