from typing import List, Dict, Union, Optional, NamedTuple

from functools import partial
import time


COLORS: Dict[str, str] = {
    'separator': '#6c6c6c',
    'icon': '#00aaff',
    'text': '#eeeeee',
    'danger': '#ff0000',
    'warning': '#ffff00',
    'info': '#aaff00',
    'fade': '#666666'
}


class Widget:
    force_text: bool = False
    update_delay: float = 0.5
    timeout: int = 10

    name: str = ''
    instance: str = ''

    def __init__(self) -> None:
        self.timestamp: float = .0
        self._cached = self.render()

    def simple_blocks(self, icon: str, text: str, color_key: Optional[str]) -> List['Block']:
        """
        Render a single Block
        markup will be, using self.show_text:
            Icon and Text with color_key
            or
            Icon with color_key
        """
        if self.force_text or self.was_clicked:
            widgets = [Icon(text=icon), Text(text=text, color_key=color_key or 'text')]
        else:
            widgets = [Icon(text=icon, color_key=color_key or 'icon')]
        return [Block(markup=widgets, name=self.name, instance=self.instance)]

    @property
    def rendered(self) -> List['Block']:
        return self._cached

    def update(self) -> None:
        """Update internal cache"""
        self._cached = self.render()

    def render(self) -> List['Block']:
        raise NotImplementedError()

    def click(self, click) -> None:
        if click['button'] == 1:
            self.timestamp_now()
            self.update()

    def timestamp_now(self) -> None:
        self.timestamp = time.time()

    @property
    def was_clicked(self) -> bool:
        return time.time() - self.timestamp < self.timeout


class Block(NamedTuple):
    markup: List['Markup']
    name: str = ''
    instance: str = ''

    def render(self) -> Dict[str, Union[str, int, bool]]:
        text: str = ' '.join(markup.render() for markup in self.markup)
        return {
            'separator_block_width': 11,
            'separator': False,
            'markup': 'pango',
            'align': 'right',
            'full_text': text,
            'short_text': text,
            'name': self.name,
            'instance': self.instance,
        }


class Markup(NamedTuple):
    text: str
    font_weight: str = 'normal'
    font_style: str = 'normal'
    color_key: str = 'text'
    colors: Dict[str, str] = COLORS

    def render(self) -> str:
        color: str = self.colors[self.color_key]
        return f'<span font_weight="{self.font_weight}" font_style="{self.font_style}" color="{color}">{self.text}</span>'


class Simple(NamedTuple):
    blocks: List['Block']

    @property
    def rendered(self) -> List['Block']:
        return self.blocks


Separator = partial(Markup, text='\ue0b3', color_key='separator', font_weight='bold', font_style='normal')
Icon = partial(Markup, text='', color_key='icon', font_weight='bold', font_style='normal')
Text = partial(Markup, text='', color_key='text', font_weight='normal', font_style='normal')

separator_widget = Simple(blocks=[Block(markup=[Separator()])])
