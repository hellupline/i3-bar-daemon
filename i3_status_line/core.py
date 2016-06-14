#! /usr/bin/env python3

from itertools import chain
import sys
import json
import importlib

import gevent.monkey
import gevent.fileobject
import gevent.socket

flatten = chain.from_iterable


class EventHandler:
    def __init__(self, widgets):
        self.widgets_by_key = {
            (widget.name, widget.instance): widget
            for widget in widgets if widget.name
        }
        self.widgets = widgets

    def sigusr1(self):
        for widget in self.widgets:
            del widget.state

    def output_loop(self):
        protocol_headers = {'version': 1, 'click_events': True}
        print(json.dumps(protocol_headers), '\n[[]')
        while True:
            blocks = flatten(widget.state for widget in self.widgets)
            print(',', json.dumps(list(blocks)))
            sys.stdout.flush()
            gevent.sleep(.1)

    def input_loop(self):
        while True:
            event = self.read_event()
            self.send_click(event)

    def read_event(self):
        gevent.socket.wait_read(sys.stdin.fileno())  # noqa pylint: disable=no-member
        data = sys.stdin.readline()
        if data == '[\n':
            data = sys.stdin.readline()
        return json.loads(data.lstrip(','))

    def send_click(self, event):
        print(event, file=sys.stderr)
        try:
            key = event['name'], event['instance']
            widget = self.widgets_by_key[key]
        except KeyError:
            return
        try:
            widget.click(event)
        except AttributeError:
            return


def load_widget(config, data):
    module = importlib.import_module(data['module'])
    widget = getattr(module, data['object'])
    return widget(config, *data['args'], **data['kwargs'])
