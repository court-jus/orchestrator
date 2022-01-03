import random
import mido

class ChordsEmitter:
    def __init__(self, output, channel=0):
        self.available_notes = []
        self.current_note = None
        self.stopat = None
        self.step_length = 60
        self.note_duration = 5
        self.output = output
        self.channel = channel

    def tick(self, event, step):
        if not self.available_notes:
            return
        if step % self.step_length == 0:
            for note in self.available_notes:
                self.output.send(mido.Message("note_on", channel=self.channel, note=note))
            self.stopat = step + self.note_duration
        if self.stopat and self.current_note and self.stopat == step:
            for note in self.available_notes:
                self.output.send(mido.Message("note_off", channel=self.channel, note=note))
    
    def noteon(self, event, msg):
        self.available_notes.append(msg.note)
        print(self.available_notes)
