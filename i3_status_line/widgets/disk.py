import psutil
from cached_property import cached_property_with_ttl
from ..base import WidgetMixin, DEFAULT_THEME


class Widget(WidgetMixin):
    icon = ''
    fmt = '{}G'.format
    name = 'disk'

    def __init__(self, config, path='/', alert=40):
        self.instance = self.path = path
        self.alert = alert
        super().__init__(config)
        self.color, = self.pallete(['danger'])

    @cached_property_with_ttl(ttl=10)
    def state(self):
        free_space = self.free_space()
        if free_space > self.alert and self.config['hide_on_zero']:
            return ()
        return (
            self.make_icon({'text': self.icon}),
            self.make_text({
                'color': self.color,
                'text': self.fmt(free_space)
            }),
            self.make_separator(),
        )

    def free_space(self):
        return psutil.disk_usage(self.path).free // 1073741824  # 1024**3 (Gb)


if __name__ == '__main__':
    print(Widget({**DEFAULT_THEME, 'hide_on_zero': False}).state)
