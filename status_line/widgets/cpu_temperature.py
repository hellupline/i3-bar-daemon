from cached_property import cached_property_with_ttl
from ..base import WidgetMixin, COLORS

THERMAL_FILE = '/sys/class/thermal/thermal_zone{}/temp'


class Widget(WidgetMixin):
    color = COLORS['danger']
    icon = '🌡'
    fmt = '{}°C'.format
    name = 'cpu-temperature'

    def __init__(self, core=0, alert=55):
        self.core = core
        self.alert = alert

    @cached_property_with_ttl(ttl=5)
    def state(self):
        temp = self.cpu_temperature()
        if temp < self.alert:
            return ()
        return (
            self.make_icon({'text': self.icon}),
            self.make_text({'color': self.color, 'text': self.fmt(temp)}),
            self.separator,
        )

    def cpu_temperature(self):
        with open(THERMAL_FILE.format(self.core)) as f:
            return int(f.read().strip()) // 1000
