import psutil
from cached_property import cached_property_with_ttl
from ..base import WidgetMixin, DEFAULT_THEME


class Widget(WidgetMixin):
    icon = ''
    fmt = '{:.2f}%'.format
    name = 'memory-load'

    def __init__(self, config, alert=80):
        self.alert = alert
        super().__init__(config)
        self.color, = self.pallete(['danger'])

    @cached_property_with_ttl(10)
    def state(self):
        load = psutil.virtual_memory().percent
        if load < self.alert and self.config['hide_on_zero']:
            return ()
        return (
            self.make_icon({'text': self.icon}),
            self.make_text({
                'color': self.color,
                'text': self.fmt(load),
            }),
            self.make_separator(),
        )


if __name__ == '__main__':
    print(Widget({**DEFAULT_THEME, 'hide_on_zero': False}).state)
