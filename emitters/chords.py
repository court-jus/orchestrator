from ..core.events import EventListener
import mido


class ChordsEmitter(EventListener):
    def __init__(self, ec, scale, output, note_duration=100):
        self.ec = ec
        ec.subscribe("tick", self.tick)
        self.scale = scale
        self.current_notes = {}
        self.note_duration = note_duration
        self.output = output
        super().__init__(ec)

    def send(self, msg):
        if not self.scale.available_notes:
            return
        if isinstance(msg, int) and msg > 0:
            # That's a tick trigger
            stopat = msg + self.note_duration
            self.current_notes.setdefault(stopat, [])
            for note in self.get_notes():
                self.output.send(mido.Message("note_on", note=note))
                self.current_notes[note] = stopat

    def tick(self, event, step):
        if self.current_notes and step in self.current_notes.values():
            for note, stopat in self.current_notes.items():
                if stopat == step:
                    self.output.send(mido.Message("note_off", note=note))

    def get_notes(self):
        scale_notes = sorted(self.scale.available_notes)
        root_note_index = scale_notes.index(self.scale.root)
        return [
            scale_notes[root_note_index + self.scale.degree + degree]
            for degree in self.scale.current_chord
        ]
