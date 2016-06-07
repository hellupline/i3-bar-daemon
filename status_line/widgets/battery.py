from cached_property import cached_property_with_ttl
from ..base import WidgetMixin

BAT_FILE = '/sys/class/power_supply/{}/{}'
fmt = '{}%'.format


class Widget(WidgetMixin):
    colors = ['#f00', '#ff0', '#af0', '#0fa', '#eee']
    icons = ['', '', '', '', '', '']
    name = 'battery'

    def __init__(self, battery='BAT0'):
        self.instance = self.battery = battery

    @cached_property_with_ttl(ttl=1)
    def state(self):
        status = self.battery_status()
        if status != 'Discharging':
            return self.get_plugged()
        return self.get_unplugged()

    def get_plugged(self):
        return self.make_icon({'text': self.icons[-1]}), self.separator

    def get_unplugged(self):
        capacity = self.battery_capacity()
        pos = capacity // 25
        return (
            self.make_icon({'text': self.icons[pos]}),
            self.make_text({'color': self.colors[pos], 'text': fmt(capacity)}),
            self.separator,
        )

    def battery_capacity(self):
        with open(BAT_FILE.format(self.battery, 'capacity')) as f:
            return int(f.read().strip())

    def battery_status(self):
        with open(BAT_FILE.format(self.battery, 'status')) as f:
            return f.read().strip()
