import alsaaudio
from cached_property import cached_property_with_ttl
from ..base import WidgetMixin, debug


class Widget(WidgetMixin):
    icons = ['', '', '']
    fmt = '{}%'.format
    name = 'audio-volume'

    def __init__(self, config, control='Master', step=5):
        self.instance = self.control = control
        self.step = step
        super().__init__(config)

    def click(self, click):
        try:
            {
                3: self.toggle_mute,
                4: self.increase,
                5: self.decrease,
            }[click['button']]()
        except KeyError:
            pass
        del self.state

    @cached_property_with_ttl(ttl=10)
    def state(self):
        mixer = self._get_mixer()
        if self.get_mute(mixer):
            return self.as_mute()
        volume = self.get_volume(mixer)
        pos = {True: 0, False: 1}[volume < 25]
        return (
            self.make_icon({'text': self.icons[pos]}),
            self.make_text({'text': self.fmt(volume)}),
            self.make_separator(),
        )

    def as_mute(self):
        color = self.pallete('fade')
        return (
            self.make_icon({'color': color, 'text': ''}),
            self.make_separator(),
        )

    def get_icon(self, volume):
        if volume < 30:
            return ''
        return '🔊'

    def toggle_mute(self):
        mixer = self._get_mixer()
        mixer.setmute(not self.get_mute(mixer))

    def get_mute(self, mixer):
        mute, *__ = mixer.getmute()
        return bool(mute)

    def get_volume(self, mixer):
        volume, *__ = mixer.getvolume()
        return volume

    def set_volume(self, mixer, value):
        try:
            mixer.setvolume(value)
        except alsaaudio.ALSAAudioError:  # noqa pylint: disable=no-member
            pass

    def increase(self):
        mixer = self._get_mixer()
        volume = self.get_volume(mixer)
        self.set_volume(mixer, volume + self.step)

    def decrease(self):
        mixer = self._get_mixer()
        volume = self.get_volume(mixer)
        self.set_volume(mixer, volume - self.step)

    def _get_mixer(self):
        return alsaaudio.Mixer(control=self.control)  # noqa pylint: disable=no-member


if __name__ == '__main__':
    debug(Widget)
