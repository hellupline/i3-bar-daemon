import psutil

from cached_property import cached_property_with_ttl
import i3_status_line.base as base

SETTINGS = {'min_width': '0000 kB/s'}


class Widget(base.WidgetMixin):
    name = 'bandwidth-meter'

    def __init__(self, theme):
        self.old_meassure = psutil.net_io_counters()
        super().__init__(theme)

    def render(self):
        current = psutil.net_io_counters()
        sent, recv = self.get_sent(current), self.get_recv(current)
        self.old_meassure = current
        return (*sent, *recv)

    def get_sent(self, current):
        sent = (current.bytes_sent - self.old_meassure.bytes_sent) // 1024
        if sent == 0:
            return ()
        return self.bandwidth_block('', sent)

    def get_recv(self, current):
        recv = (current.bytes_recv - self.old_meassure.bytes_recv) // 1024
        if recv == 0:
            return ()
        return self.bandwidth_block('', recv)

    def bandwidth_block(self, icon, text):
        icon = self._render_pango({'text': icon}, look_key='icon')
        text = self._render_pango(
            {'text': '{} kB/s'.format(text)}, look_key='text')
        return (
            self._render_block(full=icon),
            self._render_block(full=text, settings=SETTINGS),
            self._render_sep(),
        )

    @cached_property_with_ttl(ttl=1)
    def state(self):
        return self.render()


if __name__ == '__main__':
    base.debug(Widget)
