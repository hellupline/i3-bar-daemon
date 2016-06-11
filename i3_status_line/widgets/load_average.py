import os
from cached_property import cached_property_with_ttl
from ..base import WidgetMixin, DEFAULT_THEME


class Widget(WidgetMixin):
    icon = '☢'
    fmt = '{:.2f}'.format
    name = 'load-average'

    def __init__(self, config):
        super().__init__(config)
        self.color, = self.pallete(['danger'])

    @cached_property_with_ttl(ttl=1)
    def state(self):
        one, five, fifteen = os.getloadavg()
        total_cpus = os.cpu_count()
        if one < total_cpus and self.config['hide_on_zero']:
            return ()
        return (
            self.make_icon({'text': self.icon}),
            self.make_text({
                'color': self.color,
                'text': self.fmt(one),
            }),
            self.make_separator(),
        )


if __name__ == '__main__':
    print(Widget({**DEFAULT_THEME, 'hide_on_zero': False}).state)
