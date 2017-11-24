from typing import List, Optional

import psutil

from ..core import Widget, Icon, Block


class CpuLoad(Widget):
    name: str = 'cpu-load'

    def render(self) -> List[Block]:
        load_per_cpu: List[float] = psutil.cpu_percent(percpu=True)
        i, c = self.get_icon, self.get_color_key

        bars = [
            Icon(text=i(load), color_key=c(load) or 'info')
            for load in load_per_cpu
        ]
        return [Block(markup=[Icon(text=''), *bars])]

    def get_color_key(self, load: float) -> Optional[str]:
        if load > 75.0:
            return 'danger'
        elif load > 50.0:
            return 'warning'
        return None

    def get_icon(self, load: float) -> str:
        if load < 12.5:
            return '▁'
        if load < 25.0:
            return '▂'
        if load < 37.5:
            return '▃'
        if load < 50.:
            return '▄'
        if load < 62.5:
            return '▅'
        if load < 75.0:
            return '▆'
        if load < 87.2:
            return '▇'
        return '█'
