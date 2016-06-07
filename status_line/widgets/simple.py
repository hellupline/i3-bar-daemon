from cached_property import cached_property
from ..base import WidgetMixin


class Widget(WidgetMixin):
    @cached_property
    def state(self):
        return (
            self.make_icon({'text': '@'}),
            self.make_text({'text': 'hello world'}),
            self.separator,
        )
