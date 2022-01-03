import random
import mido

class RandomNoteEmitter:
    def __init__(self, output, channel=0):
        self.available_notes = []
        self.current_note = None
        self.stopat = None
        self.step_length = 15
        self.note_duration = 5
        self.output = output
        self.channel = 0

    def tick(self, event, step):
        if not self.available_notes:
            return
        if step % self.step_length == 0:
            self.current_note = random.choice(self.available_notes)
            if self.current_note:
                self.output.send(mido.Message("note_on", channel=self.channel, note=self.current_note))
                self.stopat = step + self.note_duration
        if self.stopat and self.current_note and self.stopat == step:
            self.output.send(mido.Message("note_off", channel=self.channel, note=self.current_note))
    
    def noteon(self, event, msg):
        self.available_notes.append(msg.note)
        print(self.available_notes)
