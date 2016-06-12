from cached_property import cached_property_with_ttl
from ..base import WidgetMixin, debug

BAT_FILE = '/sys/class/power_supply/{}/{}'


class Widget(WidgetMixin):
    fmt = '{}%'.format
    name = 'battery-monitor'

    def __init__(self, config, battery='BAT0'):
        self.instance = self.battery = battery
        super().__init__(config)

    @cached_property_with_ttl(ttl=1)
    def state(self):
        capacity = self.battery_capacity()
        if self.battery_status() != 'Discharging':
            return self.as_charging(capacity)
        return (
            self.make_icon({'text': self.get_icon(capacity)}),
            self.make_text({
                'color': self.get_color(capacity),
                'text': self.fmt(capacity),
            }),
            self.make_separator(),
        )

    def as_charging(self, capacity):
        return (
            self.make_icon({'text': ''}),
            self.make_separator(),
        )

    def get_color(self, capacity):
        if capacity < 20:
            return self.pallete('danger')
        elif capacity < 60:
            return self.pallete('warning')
        elif capacity < 80:
            return self.pallete('info')
        return self.pallete('text')

    def get_icon(self, capacity):
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


if __name__ == '__main__':
    debug(Widget)
