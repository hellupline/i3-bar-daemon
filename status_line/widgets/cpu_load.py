import psutil
from cached_property import cached_property_with_ttl
from ..base import WidgetMixin, COLORS

STAT_FILE = '/proc/stat'


class Widget(WidgetMixin):
    color = COLORS['danger']
    icon = '☢'
    fmt = '{:.2f}%'.format
    name = 'cpu-load'

    def __init__(self, alert=50):
        self.alert = alert

    @cached_property_with_ttl(1)
    def state(self):
        load = psutil.cpu_percent()
        if load < self.alert:
            return ()
        return (
            self.make_icon({'text': self.icon}),
            self.make_text({'color': self.color, 'text': self.fmt(load)}),
            self.separator,
        )
