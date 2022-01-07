from ..events import EventChannel
from . import Scale, Clock
from ..ui import Menu


class Controller:
    def __init__(self, debug=False):
        self.ec = EventChannel(debug)
        self.clock = Clock(self.ec)
        self.scale = Scale(self.ec)
        self.menu = Menu(self.ec, self.scale)


global_controller = Controller()
