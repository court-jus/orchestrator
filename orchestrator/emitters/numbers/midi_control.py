from ...events.listener import EventListener
from .value import Value
from ...master.controller import global_controller


class MidiControl(EventListener, Value):
    def __init__(self, ec, channel, control, initial):
        self.channel = channel
        self.control = control
        super().__init__(ec)
        if self.ec:
            self.ec.subscribe("control_change", self.control_change)
        self.save_id = f"cc_{self.channel}_{self.control}"
        self.value = global_controller.loaded.get(self.save_id, initial)
        global_controller.savables[self.save_id] = self

    def __call__(self):
        print("use value", self.value)
        return self.value

    def save(self):
        return self.value

    def control_change(self, _evt, msg):
        if not (msg.channel == self.channel and msg.control == self.control):
            return
        print("set value to", msg.value)
        self.value = msg.value
