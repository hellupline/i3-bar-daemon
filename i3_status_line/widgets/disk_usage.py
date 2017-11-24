from typing import List

import psutil

from ..core import Widget, Block


class DiskUsage(Widget):
    name: str = 'disk-usage'

    def __init__(self, path: str) -> None:
        self.instance = self.path = path
        super().__init__()

    def render(self) -> List[Block]:
        usage = psutil.disk_usage(self.path)
        c = self.get_color_key
        text = f'{self.path}: {usage.free // 1073741824} gB'
        return self.simple_blocks(icon='', text=text, color_key=c(usage))

    def get_color_key(self, usage) -> str:
        if usage.percent < 10.0:
            return 'danger'
        elif usage.percent < 25.0:
            return 'warning'
        return 'info'
