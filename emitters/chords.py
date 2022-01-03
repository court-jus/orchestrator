from ..core.events import EventListener
import mido


class ChordsEmitter(EventListener):
    def __init__(self, ec, scale, output, channel=0):
        self.ec = ec
        self.scale = scale
        self.current_notes = []
        self.stopat = None
        self.step_length = 60
        self.note_duration = 5
        self.chord = [0, 2, 4, 7]
        self.output = output
        self.channel = channel
        super().__init__(ec)

    def tick(self, event, step):
        if not self.scale.available_notes:
            return
        if step % self.step_length == 0:
            for note in self.get_notes():
                self.output.send(
                    mido.Message("note_on", channel=self.channel, note=note)
                )
                self.current_notes.append(note)
            self.stopat = step + self.note_duration
        if self.stopat and self.stopat == step:
            for note in self.current_notes:
                self.output.send(
                    mido.Message("note_off", channel=self.channel, note=note)
                )

    def get_notes(self):
        scale_notes = sorted(self.scale.available_notes)
        return [scale_notes[degree] for degree in self.chord]
