import json
import logging
import os

from ..events.listener import EventListener

from . import Clock, Scale
from ..events import EventChannel
from ..ui import Menu

logger = logging.getLogger("Controller")


class Controller(EventListener):
    def __init__(self, debug=False):
        self.savables = {}
        self.loaded = {}
        if os.path.exists("save.json"):
            with open("save.json", "r") as fp:
                self.loaded = json.load(fp)
        ec = EventChannel(debug)
        super().__init__(ec)
        self.clock = Clock(self.ec)
        self.scale = Scale(self)
        self.menu = Menu(self)
        self.opened_ports = []
        self.ec.subscribe("tick", self.tick)
        self.ec.subscribe("close", self.close_all_ports)

    def tick(self, _evt, step, *_a, **_kw):
        if step % 100 == 0:
            logger.debug("save")
            self.save()

    def save(self):
        with open("save.json", "w") as fp:
            json.dump(
                {name: savable.save() for name, savable in self.savables.items()},
                fp,
                indent=2,
            )

    def close_all_ports(self, *_args):
        for port in self.opened_ports:
            if port:
                logger.debug(f"Closing port {port}")
                port.close()
                logger.debug(f"Port {port} closed")


global_controller = Controller(True)
