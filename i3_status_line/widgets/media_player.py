import html
from cached_property import cached_property_with_ttl
from mpris2 import get_players_uri, Player
from ..base import WidgetMixin, debug


class Widget(WidgetMixin):
    name = 'media-player'

    def __init__(self, config, player='', fmt='{artist} - {title}'):
        self.instance = self.player = player
        self.fmt = fmt.format_map
        super().__init__(config)

    def click(self, click):
        try:
            {
                1: self.previous,
                2: self.play_pause,
                3: self.next,
            }[click['button']]()
        except KeyError:
            pass

    @cached_property_with_ttl(ttl=1)
    def state(self):
        metadata = self.get_metadata()
        if not metadata and self.show():
            return ()
        metadata = {'artist': '', 'album': '', 'title': '', **metadata}
        return (
            self.make_icon({'text': '♪'}),
            self.make_text({'text': self.fmt(metadata)}),
            self.make_separator(),
        )

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


if __name__ == '__main__':
    debug(Widget)
