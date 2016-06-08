from subprocess import check_output, CalledProcessError
from cached_property import cached_property_with_ttl
from ..base import WidgetMixin, COLORS


class Widget(WidgetMixin):
    color = COLORS['fade']
    icon = ''
    name = 'wifi-ssid'

    @cached_property_with_ttl(ttl=5)
    def state(self):
        ssid = self.get_ssid()
        if not ssid:
            return self.get_icon_no_ssid()
        return (
            self.make_icon({'text': self.icon}),
            self.make_text({'text': ssid}),
            self.separator,
        )

    def get_icon_no_ssid(self):
        return (
            self.make_icon({'text': self.icon, 'color': self.color}),
            self.separator
        )

    def get_ssid(self):
        try:
            return check_output(['iwgetid', '-r']).decode().strip()
        except CalledProcessError:
            return ''
