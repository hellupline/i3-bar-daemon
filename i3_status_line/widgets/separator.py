from cached_property import cached_property
import i3_status_line.base as base


class Widget(base.WidgetMixin):
    def render(self):
        return (self._render_sep(),)

    @cached_property
    def state(self):
        return self.render()


if __name__ == '__main__':
    base.debug(Widget)
