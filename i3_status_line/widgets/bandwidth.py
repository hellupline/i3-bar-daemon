import psutil
from cached_property import cached_property_with_ttl
from ..base import WidgetMixin, DEFAULT_THEME

SETTINGS = {'min_width': '0000 kB/s'}


class Widget(WidgetMixin):
    fmt = '{} kB/s'.format
    name = 'bandwidth-mether'

    def __init__(self, config):
        self.old_meassure = psutil.net_io_counters()
        super().__init__(config)

    @cached_property_with_ttl(ttl=1)
    def state(self):
        current = psutil.net_io_counters()
        sent, recv = self.get_sent(current), self.get_recv(current)
        self.old_meassure = current
        return (*sent, *recv)

    def get_sent(self, current):
        sent = (current.bytes_sent - self.old_meassure.bytes_sent) // 1024
        if sent == 0 and self.config['hide_on_zero']:
            return ()
        return (
            self.make_icon({'text': ''}),
            self.make_text({'text': self.fmt(sent)}, settings=SETTINGS),
            self.make_separator(),
        )

    def get_recv(self, current):
        recv = (current.bytes_recv - self.old_meassure.bytes_recv) // 1024
        if recv == 0 and self.config['hide_on_zero']:
            return ()
        return (
            self.make_icon({'text': ''}),
            self.make_text({'text': self.fmt(recv)}, settings=SETTINGS),
            self.make_separator(),
        )


if __name__ == '__main__':
    print(Widget({**DEFAULT_THEME, 'hide_on_zero': False}).state)
