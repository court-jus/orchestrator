from ..events.listener import EventListener
from ..emitters import Value


class Track(EventListener):
    def __init__(self, ec, gate, notes, output, mute=Value(False)):
        print("Track created", id(ec), gate, notes, output, mute)
        self.gate = gate
        self.notes = notes
        self.output = output
        self.mute = mute
        super().__init__(ec)
        self.ec.subscribe("tick", self.tick)
        self.ec.subscribe("new_song", self.clear)
        self.ec.subscribe("close", self.clear)

    def tick(self, _event, step):
        print(step, self.gate(step), self.mute())
        if self.gate(step) and not self.mute():
            note = self.notes()
            self.output(note)

    def clear(self, *args):
        for subitem in [self.gate, self.notes, self.output, self.mute]:
            subitem.clear(*args)
        self.ec.unsubscribe_all(self)
