from functools import partial, partialmethod
from cached_property import cached_property


COLORS = {
    'icon': '#0af',
    'text': '#eee',
    'separator': '#6c6c6c',
    'info': '#af0',
    'warning': '#ff0',
    'danger': '#f00',
    'fade': '#666',
}
WIDGET = {
    'separator_block_width': 11,
    'separator': False,
    'markup': 'pango',
    'align': 'right',
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
SPAN = (
    "<span color='{color}' "
    "font_style='{style}' "
    "font_weight='{weight}'  "
    ">{text}</span>"
)


def make_block(data, look=None, extra=None):
    return {
        **WIDGET, **(extra or {}),
        'full_text': SPAN.format_map({**(look or {}), **data}),
    }


def pallete(keys):
    return [*map(COLORS.get, keys)]

make_icon = partial(make_block, look=ICON)
make_text = partial(make_block, look=TEXT)


class WidgetMixin:
    separator = make_block(SEPARATOR)
    name = instance = ''

    def make_block(self, data, look=None, extra=None):
        return make_block(data, look=look, extra={
            **(extra or {}),
            'name': self.name,
            'instance': self.instance,
        })

    make_icon = partialmethod(make_block, look=ICON)
    make_text = partialmethod(make_block, look=TEXT)


class Separator(WidgetMixin):
    @cached_property
    def state(self):
        return (self.separator,)
