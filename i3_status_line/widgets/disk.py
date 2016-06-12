import psutil
from cached_property import cached_property_with_ttl
from ..base import WidgetMixin, debug


class Widget(WidgetMixin):
    fmt = '{}G'.format
    name = 'disk'

    def __init__(self, config, path='/', alert=40):
        self.instance = self.path = path
        self.alert = alert
        super().__init__(config)

    @cached_property_with_ttl(ttl=10)
    def state(self):
        free_space = self.free_space()
        if free_space > self.alert and self.show():
            return ()
        return (
            self.make_icon({'text': ''}),
            self.make_text({
                'color': self.get_color(free_space),
                'text': self.fmt(free_space)
            }),
            self.make_separator(),
        )

    def get_color(self, free_space):
        if free_space < 40:
            self.pallete('danger')
        return self.pallete('info')

    def free_space(self):
        return psutil.disk_usage(self.path).free // 1073741824  # 1024**3 (Gb)


if __name__ == '__main__':
    debug(Widget)
