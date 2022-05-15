from ..events.listener import EventListener
from ..master.controller import global_controller


class Clock(EventListener):
    def __init__(self, ec):
        self.step = 0
        self.clock_device = None
        self.save_id = "global_clock"
        super().__init__(ec)
        if self.ec:
            self.ec.subscribe("clock", self.clock)
            self.ec.subscribe("set_clock", self.set_device)
        global_controller.savables[self.save_id] = self
        if self.save_id in global_controller.loaded:
            self.clock_device = global_controller.loaded[self.save_id]
            print("LOAD CLOCK", self.clock_device)

    def save(self):
        print("SAVE CLOCK", self.clock_device)
        return self.clock_device

    def set_device(self, _event, devicename, *_a, **_kw):
        if self.clock_device is not None:
            # TODO unsubscribe clock_device
            pass
        self.clock_device = devicename

    def clock(self, _event, _msg, *_a, **kw):
        if kw.get("midi_port_name") != self.clock_device:
            return
        self.step += 1
        if self.ec:
            self.ec.publish("tick", self.step)
