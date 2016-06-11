from datetime import datetime
from ..base import WidgetMixin, DEFAULT_THEME


class Widget(WidgetMixin):
    icon = ''
    name = 'datetime'

    def __init__(self, config, hour='%H:%M:%S', date='%a %d/%m/%Y'):
        self.hour_fmt = hour
        self.date_fmt = date
        super().__init__(config)

    @property
    def state(self):
        now = datetime.now().strftime
        return (
            self.make_icon({'text': self.icon}),
            self.make_text({'text': now(self.hour_fmt)}),
            self.make_separator(),
            self.make_text({'text': now(self.date_fmt)}),
            self.make_separator(),
        )


if __name__ == '__main__':
    print(Widget({**DEFAULT_THEME, 'hide_on_zero': False}).state)
