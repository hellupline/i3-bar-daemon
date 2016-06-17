from functools import reduce
import requests

from cached_property import cached_property_with_ttl
import i3_status_line.base as base

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


class Widget(base.WidgetMixin):
    name = 'yahoo-weather'

    def __init__(self, theme, city='Curitiba', unit='C'):
        self.instance = self.city = city
        self.unit = unit
        super().__init__(theme)

    def render(self):
        return self._render_widget(
            icon='', text='{temp}°{unit}'.format(
                temp=self.get_weather(),
                unit=self.unit
            ),
        )

    def get_weather(self):
        keys = ['query', 'results', 'channel', 'item', 'condition', 'temp']
        q = Q.format(unit=self.unit, city=self.city)
        r = requests.get(URL, params={**ARGS, 'q': q})
        return reduce(dict.get, [r.json(), *keys])

    @cached_property_with_ttl(ttl=1800)
    def state(self):
        return self.render()


if __name__ == '__main__':
    base.debug(Widget)
