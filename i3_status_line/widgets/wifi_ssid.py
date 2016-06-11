from subprocess import check_output, CalledProcessError
from cached_property import cached_property_with_ttl
from ..base import WidgetMixin, DEFAULT_THEME


class Widget(WidgetMixin):
    icon = ''
    name = 'wifi-ssid'

    def __init__(self, config):
        super().__init__(config)
        self.color, = self.pallete(['fade'])

    @cached_property_with_ttl(ttl=5)
    def state(self):
        ssid = self.get_ssid()
        if not ssid:
            return self.get_icon_no_ssid()
        return self.get_icon_ssid(ssid)

    def get_icon_no_ssid(self):
        return (
            self.make_icon({'color': self.color, 'text': self.icon}),
            self.make_separator(),
        )

    def get_icon_ssid(self, ssid):
        return (
            self.make_icon({'text': self.icon}),
            self.make_text({'text': ssid}),
            self.make_separator(),
        )

    def get_ssid(self):
        try:
            return check_output(['iwgetid', '-r']).decode().strip()
        except CalledProcessError:
            return ''


if __name__ == '__main__':
    print(Widget({**DEFAULT_THEME, 'hide_on_zero': False}).state)
