from ..events.listener import EventListener


class Clock(EventListener):
    def __init__(self, ec):
        self.step = 0
        super().__init__(ec)
        if self.ec:
            self.ec.subscribe("clock", self.clock)

    def clock(self, _event, _msg):
        self.step += 1
        if self.ec:
            self.ec.publish("tick", self.step)
