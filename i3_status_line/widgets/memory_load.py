import psutil
from cached_property import cached_property_with_ttl
from ..base import WidgetMixin, debug


class Widget(WidgetMixin):
    fmt = '{:.2f}%'.format
    name = 'memory-load'

    def __init__(self, config, alert=80):
        self.alert = alert
        super().__init__(config)

    @cached_property_with_ttl(10)
    def state(self):
        load = psutil.virtual_memory().percent
        if load < self.alert and self.show():
            return ()
        return (
            self.make_icon({'text': ''}),
            self.make_text({
                'color': self.get_color(load),
                'text': self.fmt(load),
            }),
            self.make_separator(),
        )

    def get_color(self, load):
        if load > 75:
            return self.pallete('danger')
        elif load > 50:
            return self.pallete('warning')
        return self.pallete('info')


if __name__ == '__main__':
    debug(Widget)
