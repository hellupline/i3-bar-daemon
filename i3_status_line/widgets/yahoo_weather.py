from functools import reduce
import requests
from cached_property import cached_property_with_ttl
from ..base import WidgetMixin, debug

URL = 'https://query.yahooapis.com/v1/public/yql'
ARGS = {
    'env': 'store://datatables.org/alltableswithkeys',
    'format': 'json',
}
Q = (
    'select item.condition.temp from weather.forecast '
    'where u="{unit}" and woeid in '
    '(select woeid from geo.places(1) where text="{city}")'
)


class Widget(WidgetMixin):
    fmt = '{temp}°{unit}'.format

    def __init__(self, config, city='Curitiba', unit='C'):
        self.instance = self.city = city
        self.unit = unit
        super().__init__(config)

    @cached_property_with_ttl(ttl=1800)
    def state(self):
        return (
            self.make_icon({'text': ''}),
            self.make_text({'text': self.fmt(
                temp=self.get_weather(),
                unit=self.unit
            )}),
            self.make_separator(),
        )

    def get_weather(self):
        keys = ['query', 'results', 'channel', 'item', 'condition', 'temp']
        q = Q.format(unit=self.unit, city=self.city)
        r = requests.get(URL, params={**ARGS, 'q': q})
        return reduce(dict.get, [r.json(), *keys])


if __name__ == '__main__':
    debug(Widget)
