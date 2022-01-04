from ..core.events import EventListener
import mido


class ChordsEmitter(EventListener):
    def __init__(self, ec, scale, output, note_duration=100):
        self.ec = ec
        self.scale = scale
        self.current_notes = {}
        self.note_duration = note_duration
        self.chord = [0, 2, 4, 6]
        self.base_note = 60
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
        base_note_index = scale_notes.index(self.base_note)
        return [scale_notes[base_note_index + degree] for degree in self.chord]

    def control_change(self, _event, msg):
        if msg.channel != 15:
            return
        if msg.control == 33:
            self.change_degree(msg.value)
        print(msg)

    def change_degree(self, value):
        value = min(126, value)
        degrees = len(self.scale.base_notes)
        new_degree = self.scale.base_notes[int(value * degrees / 127)]
        self.base_note = new_degree
        print("nd", new_degree, self.get_notes())
