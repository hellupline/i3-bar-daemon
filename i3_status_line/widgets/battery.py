from typing import List

import psutil

from ..core import Widget, Block


class Battery(Widget):
    name = 'battery'

    def render(self) -> List[Block]:
        battery = psutil.sensors_battery()
        i, c = self.get_icon, self.get_color_key
        text = f'{battery.percent:.0f}%'
        return self.simple_blocks(icon=i(battery), text=text, color_key=c(battery))

    def get_color_key(self, battery) -> str:
        if battery.percent < 25:
            return 'danger'
        elif battery.percent < 75:
            return 'warning'
        return 'info'

    def get_icon(self, battery) -> str:
        if battery.power_plugged:
            return ''
        if battery.percent < 20:
            return ''
        elif battery.percent < 40:
            return ''
        elif battery.percent < 60:
            return ''
        elif battery.percent < 80:
            return ''
        return ''
