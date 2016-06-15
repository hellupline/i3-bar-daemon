from datetime import datetime
import i3_status_line.base as base


class Widget(base.WidgetMixin):
    name = 'datetime'

    def __init__(self, theme, hour='%H:%M:%S', date='%a %d/%m/%Y'):
        self.hour_fmt = hour
        self.date_fmt = date
        super().__init__(theme)

    def render(self):
        now = datetime.now().strftime
        icon = self._render_pango({'text': ''}, look_key='icon')
        hour = self._render_pango(
            {'text': now(self.hour_fmt)}, look_key='text')
        date = self._render_pango(
            {'text': now(self.date_fmt)}, look_key='text')
        return (
            self._render_block(full=icon),
            self._render_block(full=hour),
            self._render_sep(),
            self._render_block(full=date),
            self._render_sep(),
        )

    @property
    def state(self):
        return self.render()


if __name__ == '__main__':
    base.debug(Widget)
