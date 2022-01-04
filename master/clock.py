from ..core.events import EventListener


class Clock(EventListener):
    def __init__(self, ec):
        self.ec = ec
        self.ec.subscribe("clock", self.clock)
        self.step = 0
        super().__init__(ec)

    def clock(self, _event, _msg):
        self.step += 1
        self.ec.publish("tick", self.step)
