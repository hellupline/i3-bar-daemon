import os
from cached_property import cached_property_with_ttl
from ..base import WidgetMixin, debug


class Widget(WidgetMixin):
    fmt = '{:.2f}'.format
    name = 'load-average'

    @cached_property_with_ttl(ttl=1)
    def state(self):
        one, five, fifteen = os.getloadavg()
        total_cpus = os.cpu_count()
        if one < total_cpus and self.show():
            return ()
        return (
            self.make_icon({'text': '☢'}),
            self.make_text({
                'color': self.get_color(one, total_cpus),
                'text': self.fmt(one),
            }),
            self.make_separator(),
        )

    def get_color(self, value, total_cpus):
        if value > total_cpus:
            return self.pallete('danger')
        return self.pallete('info')


if __name__ == '__main__':
    debug(Widget)
