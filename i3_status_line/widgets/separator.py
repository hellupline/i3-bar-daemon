from cached_property import cached_property
from ..base import WidgetMixin, DEFAULT_THEME


class Widget(WidgetMixin):
    icon = '@'

    @cached_property
    def state(self):
        return (self.make_separator(),)


if __name__ == '__main__':
    print(Widget({**DEFAULT_THEME, 'hide_on_zero': False}).state)
