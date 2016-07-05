from subprocess import check_output, CalledProcessError

from cached_property import cached_property_with_ttl
import i3_status_line.base as base


class Widget(base.WidgetMixin):
    name = 'wifi-ssid'

    def render(self):
        ssid = self.get_ssid()
        return self._render_widget(
            color=self.get_color(ssid),
            icon='', text=ssid,
            icon_only=not self.show_text,
        )

    def get_color(self, ssid):
        if not ssid:
            return self._color('fade')

    def get_ssid(self):
        try:
            return check_output(['iwgetid', '-r']).decode().strip()
        except CalledProcessError:
            return ''

    @cached_property_with_ttl(ttl=5)
    def state(self):
        return self.render()


if __name__ == '__main__':
    base.debug(Widget)
