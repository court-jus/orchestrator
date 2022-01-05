from ..core.events import EventListener
import random
import mido


class RandomNoteEmitter(EventListener):
    def __init__(self, ec, scale, output, range=(0, 127)):
        self.ec = ec
        ec.subscribe("tick", self.tick)
        ec.subscribe("control_change", self.control_change)
        self.scale = scale
        self.note_duration = 5
        self.current_note = None
        self.stopat = None
        self.output = output
        self.range_size = (range[1] - range[0]) / 2
        self.range_center = (range[1] + range[0]) / 2
        self.compute_range()
        super().__init__(ec)

    def send(self, msg):
        if not self.scale.available_notes or not msg or not self.range:
            return
        range_notes = [
            n
            for n in self.scale.available_notes
            if n >= self.range[0] and n <= self.range[1]
        ]
        if not range_notes:
            # Find the available note that is the closest to the range
            self.current_note = int(
                self.range[0]
                - min([abs(self.range[0] - n) for n in self.scale.available_notes])
            )
        else:
            self.current_note = random.choice(range_notes)

        self.output.send(mido.Message("note_on", note=self.current_note))
        self.stopat = msg + self.note_duration

    def tick(self, _event, step):
        if self.stopat and self.current_note is not None and self.stopat == step:
            self.output.send(mido.Message("note_off", note=self.current_note))

    def control_change(self, event, msg):
        if msg.channel != 15:
            return
        if msg.control == 32:
            self.change_range_position(msg.value)
        elif msg.control == 24:
            self.change_range_size(msg.value)

    def change_range_position(self, value):
        self.range_center = min(max(value, self.range_size), 127 - self.range_size)
        self.compute_range()

    def change_range_size(self, value):
        self.range_size = max(1, value) / 2
        self.compute_range()

    def compute_range(self):
        low_value = max(0, self.range_center - self.range_size)
        high_value = min(127, self.range_center + self.range_size)
        if high_value < low_value + 1:
            high_value = low_value + 1
        self.range = (
            low_value,
            high_value,
        )
        print(self.range)
