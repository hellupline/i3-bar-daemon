from typing import Dict, Tuple

import json
import sys
import time

from .core import Widget, separator_widget


def read_stdin(widgets: Dict[Tuple[str, str], Widget]):
    for line in sys.stdin:
        try:
            event = json.loads(line.lstrip(','))
        except json.JSONDecodeError:
            pass
        else:
            click(widgets, event)


def click(widgets: Dict[Tuple[str, str], Widget], event: Dict[str, str]) -> None:
    key = event['name'], event['instance']
    try:
        widget = widgets[key]
    except KeyError:
        return
    try:
        widget.click(event)
    except AttributeError:
        return


def refresh(widget: Widget):
    while True:
        time.sleep(widget.update_delay)
        widget.update()  # pylint: disable=pointless-statement
