import os
import json
from ..events import EventChannel
from . import Scale, Clock
from ..ui import Menu


class Controller:
    def __init__(self, debug=False):
        self.savables = {}
        self.loaded = {}
        if os.path.exists("save.json"):
            with open("save.json", "r") as fp:
                self.loaded = json.load(fp)
        self.ec = EventChannel(debug)
        self.clock = Clock(self.ec)
        self.scale = Scale(self)
        self.menu = Menu(self)
        self.ec.subscribe("tick", self.tick)

    def tick(self, _evt, step, *_a, **_kw):
        if step % 100 == 0:
            print("save")
            self.save()

    def save(self):
        with open("save.json", "w") as fp:
            json.dump(
                {name: savable.save() for name, savable in self.savables.items()},
                fp,
                indent=2,
            )


global_controller = Controller()
