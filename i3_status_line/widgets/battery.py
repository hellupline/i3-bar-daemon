from cached_property import cached_property_with_ttl
from ..base import WidgetMixin, DEFAULT_THEME

BAT_FILE = '/sys/class/power_supply/{}/{}'


class Widget(WidgetMixin):
    color_keys = ['danger', 'warning', 'warning', 'info', 'text']
    icons = ['', '', '', '', '', '']
    fmt = '{}%'.format
    name = 'battery-monitor'

    def __init__(self, config, battery='BAT0'):
        self.instance = self.battery = battery
        super().__init__(config)
        self.colors = self.pallete(self.color_keys)

    @cached_property_with_ttl(ttl=1)
    def state(self):
        capacity = self.battery_capacity()
        status = self.battery_status()
        pos = capacity // 25
        if status != 'Discharging':
            return self.charging(capacity, pos)
        return self.discharging(capacity, pos)

    def charging(self, capacity, pos):
        return (
            self.make_icon({'text': self.icons[-1]}),
            self.make_separator(),
        )

    def discharging(self, capacity, pos):
        return (
            self.make_icon({'text': self.icons[pos]}),
            self.make_text({
                'color': self.colors[pos],
                'text': self.fmt(capacity),
            }),
            self.make_separator(),
        )

    def battery_capacity(self):
        with open(BAT_FILE.format(self.battery, 'capacity')) as f:
            return int(f.read().strip())

    def battery_status(self):
        with open(BAT_FILE.format(self.battery, 'status')) as f:
            return f.read().strip()


if __name__ == '__main__':
    print(Widget(DEFAULT_THEME).state)
