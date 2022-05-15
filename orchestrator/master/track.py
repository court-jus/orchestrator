from .controller import global_controller
from ..emitters import Value


class Track:
    def __init__(self, gate, notes, output, mute=Value(False)):
        self.gate = gate
        self.notes = notes
        self.output = output
        self.mute = mute
        global_controller.ec.subscribe("tick", self.tick)

    def tick(self, _evt, step, *_a, **_kw):
        if self.gate(step) and not self.mute():
            note = self.notes()
            self.output(note)
