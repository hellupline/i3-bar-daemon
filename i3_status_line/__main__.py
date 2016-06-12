from functools import partial
import json
import os
import signal
import argparse

import gevent

from .core import EventHandler, load_widget


parser = argparse.ArgumentParser()
parser.add_argument(
    '--config', '-c', dest='config',
    default=os.path.expanduser('~/.i3-status-line.conf'),
)


def main():
    args = parser.parse_args()

    with open(args.config) as f:
        config = json.load(f)

    loader = partial(load_widget, config['config'])
    widgets = list(map(loader, config['widgets']))

    handler = EventHandler(widgets)
    signal.signal(signal.SIGUSR1, handler.sigusr1)

    try:
        gevent.joinall([
            gevent.spawn(handler.output_loop),
            gevent.spawn(handler.input_loop),
        ])
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()