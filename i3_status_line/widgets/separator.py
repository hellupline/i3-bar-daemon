from cached_property import cached_property
from ..base import WidgetMixin, debug


class Widget(WidgetMixin):
    @cached_property
    def state(self):
        return (self.make_separator(),)


if __name__ == '__main__':
    debug(Widget)
