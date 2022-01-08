import mido
from ...events.listener import EventListener


class NoteEmitter(EventListener):
    def __init__(self, ec):
        super().__init__(ec)
        self.current_notes = {}
        if self.ec:
            ec.subscribe("tick", self.tick)

    def tick(self, event, step):
        if self.current_notes and step in self.current_notes.values():
            for note, stopat in self.current_notes.items():
                if stopat == step:
                    self.output.send(mido.Message("note_off", note=note))
