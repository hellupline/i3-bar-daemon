from typing import List, Tuple

from contextlib import contextmanager

import psutil

from ..core import Widget, Icon, Text, Separator, Block


class NetworkBandwidth(Widget):
    name = 'network-bandwidth'

    def __init__(self) -> None:
        self.old_meassure = psutil.net_io_counters()
        super().__init__()

    def render(self) -> List[Block]:
        sent, recv = self.get_measures()
        sent_icon, sent_text = Icon(text=''), Text(text=f'{sent} kB/s')
        recv_icon, recv_text = Icon(text=''), Text(text=f'{recv} kB/s')
        separator = Separator()
        return [
            Block(markup=[sent_icon, sent_text]),
            Block(markup=[Separator()]),
            Block(markup=[recv_icon, recv_text]),
        ]

    @contextmanager
    def _update_value(self):
        current_meassure = psutil.net_io_counters()
        yield current_meassure
        self.old_meassure = current_meassure

    def get_measures(self) -> Tuple[int, int]:
        with self._update_value() as current_meassure:
            return self.get_sent(current_meassure), self.get_recv(current_meassure)

    def get_sent(self, current_meassure) -> int:
        return (current_meassure.bytes_sent - self.old_meassure.bytes_sent) // 1024

    def get_recv(self, current_meassure) -> int:
        return (current_meassure.bytes_recv - self.old_meassure.bytes_recv) // 1024
