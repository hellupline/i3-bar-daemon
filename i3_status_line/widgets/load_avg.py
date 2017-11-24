from typing import List

import os

from ..core import Widget, Block


class LoadAvg(Widget):
    name: str = 'load-average'

    def render(self) -> List[Block]:
        one, five, fifteen = os.getloadavg()
        cpu_count = os.cpu_count()
        c = self.get_color_key
        return self.simple_blocks(icon='', text=f'{one:.2f}', color_key=c(one, cpu_count))

    def get_color_key(self, value: float, total_cpus: int) -> str:
        if value > total_cpus:
            return 'danger'
        return 'info'
