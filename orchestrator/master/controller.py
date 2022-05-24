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
        self.loaded_song = None
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
        self.ec.subscribe("loadsong", self.loadsong)
        self.ec.subscribe("new_song", self.new_song)

    def postinit(self):
        if "song" in self.loaded:
            self.ec.publish("loadsong", self.loaded["song"])
        for port in self.loaded.get("opened_ports", []):
            self.ec.publish("choose_port", *port)

    def tick(self, _event, step):
        if step % 100 == 0:
            logger.debug("save")
            self.save()

    def save(self):
        save = {name: savable.save() for name, savable in self.savables.items()}
        save.update({"opened_ports": []})
        for port in self.opened_ports:
            if isinstance(port, dict):
                save["opened_ports"].append(
                    [
                        "choose",
                        port["direction"],
                        port["filtered_events"],
                        port["portname"],
                    ]
                )
        if self.loaded_song:
            save["song"] = self.loaded_song
        with open("save.json", "w") as fp:
            json.dump(
                save,
                fp,
                indent=2,
            )

    def close_all_ports(self, *_args):
        for port in self.opened_ports:
            if not isinstance(port, dict) and port:
                logger.debug(f"Closing port {port}")
                port.close()
                logger.debug(f"Port {port} closed")

    def loadsong(self, _event, filename):
        from ..song import loadsong

        opened_ports, song = loadsong(os.path.join("songs", filename), self)
        self.opened_ports.extend(opened_ports)
        self.loaded_song = filename
        logger.info(f"Song loaded: {filename}")

    def new_song(self, _event):
        logger.info(f"New empty song")
        self.loaded_song = None


global_controller = Controller(True)
