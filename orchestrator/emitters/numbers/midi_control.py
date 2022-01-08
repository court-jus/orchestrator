from ...events.listener import EventListener
from .value import Value


class MidiControl(EventListener, Value):
    def __init__(self, ec, channel, control, initial):
        self.channel = channel
        self.control = control
        self.value = initial
        super().__init__(ec)
        if self.ec:
            self.ec.subscribe("control_change", self.control_change)

    def __call__(self):
        print("use value", self.value)
        return self.value

    def control_change(self, _evt, msg):
        if not (msg.channel == self.channel and msg.control == self.control):
            return
        print("set value to", msg.value)
        self.value = msg.value
