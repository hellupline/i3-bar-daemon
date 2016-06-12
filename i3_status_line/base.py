import json


BASE_BLOCK_SETTINGS = {
    'separator_block_width': 11,
    'separator': False,
    'markup': 'pango',
    'align': 'right',
}
SPAN = (
    "<span color='{color}'"
    " font_style='{style}'"
    " font_weight='{weight}'"
    ">{text}</span>"
)
COLORS = {
    'separator': '#6c6c6c',
    'icon': '#0af',
    'text': '#eee',
    'danger': '#f00',
    'warning': '#ff0',
    'info': '#af0',
    'fade': '#666',
}
SEPARATOR = {
    'color': COLORS['separator'],
    'style': 'normal',
    'weight': 'bold',
    'text': '\ue0b3',
}
ICON = {
    'color': COLORS['icon'],
    'style': 'normal',
    'weight': 'bold',
}
TEXT = {
    'color': COLORS['text'],
    'style': 'normal',
    'weight': 'normal',
}
DEFAULT_THEME = {'hide_on_zero': True, 'theme': {
    'separator': SEPARATOR,
    'icon': ICON,
    'text': TEXT,
    'colors': COLORS,
}}


class WidgetMixin:
    name = instance = ''
    state = ()

    def __init__(self, config):
        self.config = config

    def pallete(self, key):
        return self.config['theme']['colors'][key]

    def show(self):
        return self.config['hide_on_zero']

    def _make_block(self, block, theme=None, settings=None):
        return make_block(block, theme=theme, settings={
            'name': self.name,
            'instance': self.instance,
            **(settings or {}),
        })

    def make_separator(self, theme=None, settings=None):
        return self._make_block(block={}, settings=settings, theme={
            **self.config['theme']['separator'],
            **(theme or {}),
        })

    def make_icon(self, block, theme=None, settings=None):
        return self._make_block(block, settings=settings, theme={
            **self.config['theme']['icon'],
            **(theme or {}),
        })

    def make_text(self, block, theme=None, settings=None):
        return self._make_block(block, settings=settings, theme={
            **self.config['theme']['text'],
            **(theme or {}),
        })


def make_block(block, theme, settings):
    return {
        **BASE_BLOCK_SETTINGS, **(settings or {}),
        'full_text': SPAN.format_map({
            **(theme or {}), **block,
        })
    }


def debug(widget_class):
    widget = widget_class({**DEFAULT_THEME, 'hide_on_zero': False})
    print(json.dumps(widget.state, indent=4))
