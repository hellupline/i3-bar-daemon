from datetime import datetime
from ..base import WidgetMixin, debug


class Widget(WidgetMixin):
    name = 'datetime'

    def __init__(self, config, hour='%H:%M:%S', date='%a %d/%m/%Y'):
        self.hour_fmt = hour
        self.date_fmt = date
        super().__init__(config)

    @property
    def state(self):
        now = datetime.now().strftime
        return (
            self.make_icon({'text': ''}),
            self.make_text({'text': now(self.hour_fmt)}),
            self.make_separator(),
            self.make_text({'text': now(self.date_fmt)}),
            self.make_separator(),
        )


if __name__ == '__main__':
    debug(Widget)
