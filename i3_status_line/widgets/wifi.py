from typing import List, Tuple

from subprocess import check_output, CalledProcessError

from ..core import Widget, Block


class Wifi(Widget):
    name = 'wifi'

    def render(self) -> List[Block]:
        ssid, signal = self.get_wifi_details()
        c = self.get_color_key
        return self.simple_blocks(icon='', text=f'{ssid} {signal}%', color_key=c(signal))

    def get_color_key(self, signal: int) -> str:
        if signal == 0:
            return 'fade'
        if signal < 25:
            return 'danger'
        if signal < 50:
            return 'warning'
        return 'info'

    def get_wifi_details(self) -> Tuple[str, int]:
        try:
            result: bytes = check_output([
                'nmcli',
                '--mode', 'tabular',
                '--colors', 'no',
                '--terse',
                '--fields', 'in-use,ssid,signal',
                'device', 'wifi', 'list',
            ])
        except CalledProcessError:
            pass
        else:
            for row in result.decode().splitlines():
                in_use, ssid, signal = row.split(':')
                if in_use == '*':
                    return ssid, int(signal)
        return ('', 0)
