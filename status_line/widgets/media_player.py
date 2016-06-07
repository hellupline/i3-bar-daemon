import html
from cached_property import cached_property_with_ttl
from mpris2 import get_players_uri, Player
from ..base import WidgetMixin


class Widget(WidgetMixin):
    fmt = '{album} - {title}'.format_map
    name = 'media-player'

    def __init__(self, player=''):
        self.instance = self.player = player

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
        if not metadata:
            return ()
        return (
            self.make_icon({'text': '♪'}),
            self.make_text({'text': self.fmt(metadata)}),
            self.separator,
        )

    def get_metadata(self):
        # pylint: disable=unsubscriptable-object
        try:
            metadata = self.get_player().Metadata
        except StopIteration:
            return {}
        return {
            'artist': html.escape(', '.join(metadata['xesam:artist'])),
            'album': html.escape(str(metadata['xesam:album'])),
            'title': html.escape(str(metadata['xesam:title'])),
        }

    def get_player(self):
        # pylint: disable=unexpected-keyword-arg
        uri = next(get_players_uri('.+{}'.format(self.player)))
        return Player(dbus_interface_info={'dbus_uri': uri})

    def previous(self):
        self.get_player().Previous()

    def next(self):
        self.get_player().Next()

    def play_pause(self):
        self.get_player().PlayPause()
