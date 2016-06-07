import pulsectl
from cached_property import cached_property_with_ttl
from ..base import WidgetMixin


class Widget(WidgetMixin):
    color = '#666'
    icons = ['', '🔊', '']
    fmt = '{}%'.format
    name = 'audio-volume'

    def __init__(self, step=5):
        self.pulse = pulsectl.Pulse('i3-audio-watcher')
        self.sink = self.pulse.sink_list()[0]
        self.step = step

    def click(self, click):
        try:
            {
                3: self.mute_unmute,
                4: self.increase,
                5: self.decrease,
            }[click['button']]()
        except KeyError:
            return
        del self.state

    @cached_property_with_ttl(ttl=10)
    def state(self):
        volume = self.volume
        if volume == 'MUTE':
            return self.show_as_mute()
        pos = {True: 0, False: 1}[volume < 25]
        return (
            self.make_icon({'text': self.icons[pos]}),
            self.make_text({'text': self.fmt(volume)}),
            self.separator,
        )

    def show_as_mute(self):
        return (
            self.make_icon({'color': self.color, 'text': self.icons[-1]}),
            self.separator,
        )

    @property
    def volume(self):
        if self.sink.mute:
            return 'MUTE'
        volume = self.pulse.volume_get_all_chans(self.sink)
        return round(volume * 100)

    @volume.setter
    def volume(self, value):
        if not 0 <= value <= 100:
            return
        volume = self.pulse.volume_set_all_chans(self.sink, value / 100)

    def mute_unmute(self):
        self.pulse.mute(self.sink, mute=not self.sink.mute)

    def increase(self):
        self.volume = self.volume + self.step

    def decrease(self):
        self.volume = self.volume - self.step
