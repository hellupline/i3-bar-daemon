import os
from cached_property import cached_property_with_ttl
from ..base import WidgetMixin


class Widget(WidgetMixin):
    color = '#f00'
    icon = '☢'
    fmt = '{:.2f}'.format
    name = 'load-average'

    @cached_property_with_ttl(ttl=1)
    def state(self):
        one, five, fifteen = os.getloadavg()
        total_cpus = os.cpu_count()
        if one < total_cpus:
            return ()
        return (
            self.make_icon({'text': self.icon}),
            self.make_text({'color': self.color, 'text': self.fmt(one)}),
            self.separator,
        )
