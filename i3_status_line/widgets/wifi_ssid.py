from subprocess import check_output, CalledProcessError
from cached_property import cached_property_with_ttl
from ..base import WidgetMixin, debug


class Widget(WidgetMixin):
    name = 'wifi-ssid'

    @cached_property_with_ttl(ttl=5)
    def state(self):
        ssid = self.get_ssid()
        if not ssid:
            return self.as_no_ssid()
        return (
            self.make_icon({'text': ''}),
            self.make_text({'text': ssid}),
            self.make_separator(),
        )

    def as_no_ssid(self):
        return (
            self.make_icon({
                'color': self.pallete('fade'),
                'text': '',
            }),
            self.make_separator(),
        )

    def get_ssid(self):
        try:
            return check_output(['iwgetid', '-r']).decode().strip()
        except CalledProcessError:
            return ''


if __name__ == '__main__':
    debug(Widget)
