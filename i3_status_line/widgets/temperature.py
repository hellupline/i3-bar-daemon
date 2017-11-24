from typing import List, Dict, Any

import psutil

from ..core import Widget, Block


class Temperature(Widget):
    name: str = 'temperature'

    def render(self) -> List[Block]:
        sensors: Dict[str, List[Any]] = psutil.sensors_temperatures()
        sensor = sensors['coretemp'][0]
        i, c = self.get_icon, self.get_color_key
        text = f'{sensor.current:.0f}°C'
        return self.simple_blocks(icon=i(sensor), text=text, color_key=c(sensor))

    def get_color_key(self, sensor) -> str:
        if sensor.current > 60.0:
            return 'danger'
        elif sensor.current > 55.0:
            return 'warning'
        return 'info'

    def get_icon(self, sensor) -> str:
        if sensor.current > 60.0:
            return ''
        elif sensor.current > 55.0:
            return ''
        return ''
