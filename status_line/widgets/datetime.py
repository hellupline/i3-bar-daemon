from datetime import datetime
from ..base import WidgetMixin


class Widget(WidgetMixin):
    name = 'datetime'

    def __init__(self, hour='%H:%M:%S', date='%a %d/%m/%Y'):
        self.hour_fmt = hour
        self.date_fmt = date

    @property
    def state(self):
        now = datetime.now().strftime
        return (
            self.make_icon({'text': '🕜'}),
            self.make_text({'text': now(self.hour_fmt)}),
            self.separator,
            self.make_text({'text': now(self.date_fmt)}),
            self.separator,
        )
