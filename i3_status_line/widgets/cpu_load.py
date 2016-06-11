import psutil
from cached_property import cached_property_with_ttl
from ..base import WidgetMixin, DEFAULT_THEME


class Widget(WidgetMixin):
    icon = ''
    fmt = '{:.2f}%'.format
    name = 'cpu-load'

    def __init__(self, config, alert=30):
        self.alert = alert
        super().__init__(config)
        self.colors = self.pallete(['info', 'warning', 'danger'])

    @cached_property_with_ttl(1)
    def state(self):
        load = psutil.cpu_percent()
        if load < self.alert and self.config['hide_on_zero']:
            return ()
        pos = int(load // 50)
        return (
            self.make_icon({'text': self.icon}),
            self.make_text({
                'color': self.colors[pos],
                'text': self.fmt(load),
            }),
            self.make_separator(),
        )


if __name__ == '__main__':
    print(Widget({**DEFAULT_THEME, 'hide_on_zero': False}).state)
