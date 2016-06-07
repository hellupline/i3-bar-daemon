import psutil
from cached_property import cached_property_with_ttl
from ..base import WidgetMixin

STAT_FILE = '/proc/stat'


class Widget(WidgetMixin):
    color = '#f00'
    icon = '☢'
    fmt = '{:.2f}%'.format
    name = 'memory-load'

    def __init__(self, alert=80):
        self.alert = alert

    @cached_property_with_ttl(10)
    def state(self):
        load = psutil.virtual_memory().percent
        if load < self.alert:
            return ()
        return (
            self.make_icon({'text': self.icon}),
            self.make_text({'color': self.color, 'text': self.fmt(load)}),
            self.separator,
        )
