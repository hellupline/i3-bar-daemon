import psutil
from cached_property import cached_property_with_ttl
from ..base import WidgetMixin


EXTRA_ARGS = {'min_width': '0000 kB/s'}


class Widget(WidgetMixin):
    fmt = '{} kB/s'.format
    name = 'bandwith'

    def __init__(self, interface):
        self.old_meassure = psutil.net_io_counters(pernic=True)[interface]
        self.interface = interface

    @cached_property_with_ttl(ttl=1)
    def state(self):
        current = psutil.net_io_counters(pernic=True)[self.interface]
        sent, recv = self.get_sent(current), self.get_recv(current)
        self.old_meassure = current
        return (*sent, *recv)

    def get_sent(self, current):
        sent = (current.bytes_sent - self.old_meassure.bytes_sent) // 1024
        if sent == 0:
            return ()
        return (
            self.make_icon({'text': '⬆'}),
            self.make_text({'text': self.fmt(sent)}, extra=EXTRA_ARGS),
            self.separator,
        )

    def get_recv(self, current):
        recv = (current.bytes_recv - self.old_meassure.bytes_recv) // 1024
        if recv == 0:
            return ()
        return (
            self.make_icon({'text': '⬇'}),
            self.make_text({'text': self.fmt(recv)}, extra=EXTRA_ARGS),
            self.separator,
        )
