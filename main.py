#! /usr/bin/env python3

import asyncio
import signal
import sys
import json

from status_line.base import Separator
from status_line.widgets import (
    audio_volume,
    bandwidth,
    battery,
    cpu_load,
    cpu_temperature,
    datetime,
    disk,
    load_average,
    media_player,
    wifi_ssid,
)

WIDGETS = [
    Separator(),
    bandwidth.Widget(interface='wlp7s0'),
    media_player.Widget(),

    datetime.Widget(),

    disk.Widget(path='/home/'),
    cpu_load.Widget(),
    load_average.Widget(),
    cpu_temperature.Widget(),

    battery.Widget(),
    wifi_ssid.Widget(),
    audio_volume.Widget(),
]


class EventHandler:
    def __init__(self, widgets):
        self.widgets_by_key = {
            (widget.name, widget.instance): widget
            for widget in widgets if widget.name
        }
        self.widgets = widgets

    async def handle_output(self):
        print(json.dumps({'version': 1, 'click_events': True}), '\n[[]')
        while True:
            print(',', json.dumps([
                block for widget in WIDGETS for block in widget.state
            ]))
            sys.stdout.flush()
            await asyncio.sleep(.1)

    async def handle_input(self):
        reader = await self.stream_reader()
        while True:
            data = await reader.readline()
            if data == b'[\n':
                data = await reader.readline()
            try:
                data = json.loads(data.decode().lstrip(','))
            except json.JSONDecodeError:
                continue
            try:
                key = data['name'], data['instance']
                widget = self.widgets_by_key[key]
            except KeyError:
                continue
            try:
                widget.click(data)
            except AttributeError:
                continue

    async def stream_reader(self, loop=None):
        if loop is None:
            loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        reader_protocol = asyncio.StreamReaderProtocol(reader)
        await loop.connect_read_pipe(lambda: reader_protocol, sys.stdin)
        return reader

    def sigusr1(self):
        for widget in self.widgets:
            del widget.state


def main():
    handler = EventHandler(WIDGETS)
    signal.signal(signal.SIGUSR1, handler.sigusr1)
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(asyncio.wait([
            handler.handle_input(),
            handler.handle_output(),
        ]))
    finally:
        loop.close()

if __name__ == '__main__':
    main()
