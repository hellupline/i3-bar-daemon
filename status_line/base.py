from functools import partial, partialmethod
from cached_property import cached_property


WIDGET = {
    'separator_block_width': 11,
    'separator': False,
    'markup': 'pango',
    'align': 'right',
}
ICON = {
    'color': '#00aaff',
    'style': 'normal',
    'weight': 'bold',
}
TEXT = {
    'color': '#eee',
    'style': 'normal',
    'weight': 'normal',
}
SEPARATOR = {
    'color': '#6c6c6c',
    'style': 'normal',
    'weight': 'bold',
    'text': '\ue0b3',
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
