from typing import List

from datetime import datetime

from ..core import Widget, Icon, Text, Separator, Block


class Clock(Widget):
    name = 'clock'

    def __init__(self, hour_fmt: str = '%H:%M:%S',
                 date_fmt: str = '%a %d/%m/%Y') -> None:
        self.hour_fmt = hour_fmt
        self.date_fmt = date_fmt
        super().__init__()

    def render(self) -> List[Block]:
        now = datetime.now().strftime
        time_widgets = [Icon(text=''), Text(text=now(self.hour_fmt))]
        date_widgets = [Text(text=now(self.date_fmt))]
        return [
            Block(markup=time_widgets, name=self.name, instance=self.instance),
            Block(markup=[Separator()]),
            Block(markup=date_widgets, name=self.name, instance=self.instance),
        ]
