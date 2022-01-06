from .events import EventListener


class Value:
    def __init__(self, generator):
        self.generator = generator

    def __call__(self):
        return self.generator


class MidiControl(EventListener, Value):
    def __init__(self, ec, channel, control):
        self.channel = channel
        self.control = control
        self.value = 0
        super().__init__(ec)
        if self.ec:
            self.ec.subscribe("control_change", self.control_change)

    def __call__(self):
        return self.value

    def control_change(self, _evt, msg):
        if not (msg.channel == self.channel and msg.control == self.control):
            return
        self.value = msg.value
