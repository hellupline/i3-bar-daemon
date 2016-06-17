import json


class WidgetMixin:
    use_icon_only_as_short_text = True
    name = instance = ''

    def __init__(self, theme):
        self.theme = theme
        self._looks = {
            'separator': {**SEPARATOR, **self.theme['separator']},
            'text': {**TEXT, **self.theme['text']},
            'icon': {**ICON, **self.theme['icon']},
        }

    def _render_widget(self, icon, text, color=None, icon_only=False):
        short, icon, text = {'text': icon}, {'text': icon}, {'text': text}
        if color is not None:
            short['color'], text['color'] = color, color
        full = short = self._render_pango(short, look_key='icon')
        if not icon_only:
            full = icon = self._render_pango(icon, look_key='icon')
            if text['text']:
                text = self._render_pango(text, look_key='text')
                full = '{}   {}'.format(icon, text)
        return (
            self._render_block(short=short, full=full),
            self._render_sep(),
        )

    def _render_pango(self, body, look_key):
        return SPAN({**self._looks[look_key], **body})

    def _render_block(self, full, short=None, settings=None):
        return {
            **BASE_BLOCK_SETTINGS,
            **(settings or {}),
            'full_text': full,
            'short_text': short or full,
            'name': self.name,
            'instance': self.instance,
        }

    def _render_sep(self, settings=None):
        return self._render_block(full=SPAN(SEPARATOR), settings=settings)

    def _color(self, key):
        return self.theme['colors'][key]


BASE_BLOCK_SETTINGS = {
    'separator_block_width': 11,
    'separator': False,
    'markup': 'pango',
    'align': 'right',
}
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
DEFAULT_THEME = {
    'separator': SEPARATOR,
    'icon': ICON,
    'text': TEXT,
    'colors': COLORS,
}

SPAN = (
    "<span color='{color}'"
    " font_style='{style}'"
    " font_weight='{weight}'"
    ">{text}</span>"
).format_map


def debug(widget_class):
    widget = widget_class(DEFAULT_THEME)
    print(json.dumps(widget.state, indent=4))
