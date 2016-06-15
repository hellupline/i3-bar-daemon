import html
from mpris2 import get_players_uri, Player

from cached_property import cached_property_with_ttl
import i3_status_line.base as base


class PlayerControl:
    def __init__(self, player='', fmt='{artist} - {title}'):
        self.player = player
        self.fmt = fmt.format_map

    def get_text(self):
        try:
            return self.fmt(self.get_metadata())
        except KeyError:
            return ''

    def get_metadata(self):
        # pylint: disable=unsubscriptable-object
        try:
            metadata = self.get_player().Metadata
        except AttributeError:
            return {}
        return {
            'artist': html.escape(', '.join(metadata['xesam:artist'])),
            'album': html.escape(str(metadata['xesam:album'])),
            'title': html.escape(str(metadata['xesam:title'])),
        }

    def get_player(self):
        # pylint: disable=unexpected-keyword-arg
        try:
            uri = next(get_players_uri('.+{}'.format(self.player)))
        except StopIteration:
            return
        return Player(dbus_interface_info={'dbus_uri': uri})

    def previous(self):
        try:
            self.get_player().Previous()
        except AttributeError:
            pass

    def next(self):
        try:
            self.get_player().Next()
        except AttributeError:
            pass

    def play_pause(self):
        try:
            self.get_player().PlayPause()
        except AttributeError:
            pass


class Widget(base.WidgetMixin):
    name = 'media-player'

    def __init__(self, theme, player='', fmt='{artist} - {title}'):
        self.player_control = PlayerControl(player=player, fmt=fmt)
        self.instance = player
        super().__init__(theme)

    def click(self, click):
        try:
            {
                1: self.player_control.previous,
                2: self.player_control.play_pause,
                3: self.player_control.next,
            }[click['button']]()
        except KeyError:
            pass

    def render(self):
        text = self.player_control.get_text()
        return self._render_widget(
            color=self._color('text'),
            icon='♪', text=text,
        )

    @cached_property_with_ttl(ttl=5)
    def state(self):
        return self.render()


if __name__ == '__main__':
    base.debug(Widget)
