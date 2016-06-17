import alsaaudio

from cached_property import cached_property, cached_property_with_ttl
import i3_status_line.base as base


class VolumeControl:
    def __init__(self, control='Master', step=5):
        self.control = control
        self.step = step

    def __enter__(self):
        return self

    def __exit__(self, _type, value, traceback):
        del self.mixer

    def toggle_mute(self):
        self.mute = not self.mute

    @property
    def mute(self):
        mute, *__ = self.mixer.getmute()
        return bool(mute)

    @mute.setter
    def mute(self, value):
        self.mixer.setmute(value)

    @property
    def volume(self):
        volume, *__ = self.mixer.getvolume()
        return volume

    @volume.setter
    def volume(self, value):
        try:
            self.mixer.setvolume(value)
        except alsaaudio.ALSAAudioError:  # noqa pylint: disable=no-member
            pass

    def increase(self):
        self.volume += self.step

    def decrease(self):
        self.volume -= self.step

    @cached_property
    def mixer(self):
        return alsaaudio.Mixer(control=self.control)  # noqa pylint: disable=no-member


class Widget(base.WidgetMixin):
    name = 'battery-monitor'

    def __init__(self, theme, control='Master', step=5):
        self.volume_control = VolumeControl(control=control, step=step)
        self.instance = control
        super().__init__(theme)

    def click(self, click):
        try:
            {
                3: self.volume_control.toggle_mute,
                4: self.volume_control.increase,
                5: self.volume_control.decrease,
            }[click['button']]()
        except KeyError:
            pass
        del self.state

    def render(self):
        with self.volume_control:
            volume = self.volume_control.volume
            return self._render_widget(
                color=self.get_color(),
                icon=self.get_icon(volume),
                text='{}%'.format(volume),
            )

    def get_color(self):
        if self.volume_control.mute:
            return self._color('fade')

    def get_icon(self, volume):
        if volume == 0:
            return ''
        elif volume < 30:
            return ''
        return '🔊'

    @cached_property_with_ttl(ttl=5)
    def state(self):
        return self.render()


if __name__ == '__main__':
    base.debug(Widget)
