from ..core.events import EventListener
import random
import mido


class RandomNoteEmitter(EventListener):
    def __init__(self, ec, scale, output, channel=0):
        self.ec = ec
        self.scale = scale
        self.current_note = None
        self.stopat = None
        self.step_length = 150
        self.note_duration = 5
        self.output = output
        self.channel = 0
        super().__init__(ec)

    def tick(self, event, step):
        if not self.scale.available_notes:
            return
        if step % self.step_length == 0:
            self.current_note = random.choice(self.scale.available_notes)
            self.output.send(
                mido.Message("note_on", channel=self.channel, note=self.current_note)
            )
            self.stopat = step + self.note_duration
        if self.stopat and self.current_note and self.stopat == step:
            self.output.send(
                mido.Message("note_off", channel=self.channel, note=self.current_note)
            )
