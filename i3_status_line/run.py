#! /usr/bin/env python3

from typing import Dict, Tuple

from functools import partial
from threading import Thread
import json
import sys
import time

from .widgets import NetworkBandwidth, Clock, CpuLoad, MemLoad, Temperature, Wifi, Battery
from .core import Widget, separator_widget
from .events import read_stdin, click, refresh


def main():
    network_bandwitch = NetworkBandwidth()
    clock = Clock()
    cpu_load = CpuLoad()
    men_load = MemLoad()
    temperature = Temperature()
    wifi = Wifi()
    battery = Battery()

    widgets_map = {(w.name, w.instance): w for w in [
        network_bandwitch, clock,
        cpu_load, men_load, temperature,
        wifi, battery,
    ]}

    widgets = [
        separator_widget, network_bandwitch,
        separator_widget, clock,
        separator_widget, cpu_load,
        separator_widget, men_load,
        separator_widget, temperature,
        separator_widget, wifi,
        separator_widget, battery,
        separator_widget,
    ]

    to_update = [
        Thread(
            target=partial(refresh, widget),
            daemon=True,
            name=f'{name}:{instance}',
        )
        for (name, instance), widget in widgets_map.items()
    ]
    input_loop = Thread(
        target=partial(read_stdin, widgets_map),
        daemon=True,
        name='read-stdin',
    )

    for thread in to_update:
        thread.start()
    input_loop.start()

    print_header(f_obj=sys.stdout)
    while True:
        rendered = [
            block.render()  # pylint: disable=no-member
            for widget in widgets
            for block in widget.rendered  # type: ignore
        ]
        print(f', {json.dumps(rendered)}', file=sys.stdout)
        sys.stdout.flush()
        time.sleep(.5)


def print_header(f_obj) -> None:
    print('{"version": 1, "click_events": true}\n[[]', file=f_obj)


if __name__ == '__main__':
    main()
