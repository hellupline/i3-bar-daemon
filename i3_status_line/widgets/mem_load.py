from typing import List, Optional

import psutil

from ..core import Widget, Block


class MemLoad(Widget):
    name: str = 'memory-load'

    def render(self) -> List[Block]:
        mem = psutil.virtual_memory()
        c = self.get_color_key
        return self.simple_blocks(
            icon='', text=f'{mem.used // 1024 // 1024} MB',
            color_key=c(mem.percent),
        )

    def get_color_key(self, load: float) -> Optional[str]:
        if load > 75.0:
            return 'danger'
        elif load > 50.0:
            return 'warning'
        return 'info'
