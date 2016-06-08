import psutil
from cached_property import cached_property_with_ttl
from ..base import WidgetMixin, COLORS


class Widget(WidgetMixin):
    color = COLORS['danger']
    icon = ''
    fmt = '{}G'.format
    name = 'disk'

    def __init__(self, path, alert=40):
        self.instance = self.path = path
        self.alert = alert

    @cached_property_with_ttl(ttl=10)
    def state(self):
        usage = self.disk_usage()
        if usage > self.alert:
            return ()
        return (
            self.make_icon({'text': self.icon}),
            self.make_text({'color': self.color, 'text': self.fmt(usage)}),
            self.separator,
        )

    def disk_usage(self):
        return psutil.disk_usage(self.path).free // 1073741824  # 1024**3 (Gb)
