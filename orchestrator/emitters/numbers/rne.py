import logging
import random

import mido

from ...master.controller import global_controller
from .value import Value

logger = logging.getLogger("RandomNoteEmitter")


class RandomNoteEmitter(Value):
    def __init__(
        self,
        range_center=Value(60),
        range_size=Value(6),
        note_duration=Value(5),
        velocity=Value(64),
    ):
        self.note_duration = note_duration
        self.current_note = None
        self.stopat = None
        self.range_center = range_center
        self.range_size = range_size
        self.velocity = velocity

    def __call__(self):
        if not self.scale.available_notes or not msg:
            return
        range_notes = [
            n
            for n in self.scale.available_notes
            if n >= self.get_low_boundary() and n <= self.get_high_boundary()
        ]
        if self.ec.debug:
            logger.debug("Range notes", range_notes)
        if not range_notes:
            # Find the available note that is the closest to the range
            self.current_note = int(
                self.get_low_boundary()
                - min(
                    [
                        abs(self.get_low_boundary() - n)
                        for n in self.scale.available_notes
                    ]
                )
            )
        else:
            self.current_note = random.choice(range_notes)

        self.output.send(
            mido.Message("note_on", note=self.current_note, velocity=self.velocity())
        )
        self.stopat = msg + self.note_duration()

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

    def get_range_center(self):
        return min(
            max(self.range_center(), self.get_range_size()), 127 - self.get_range_size()
        )

    def get_range_size(self):
        return max(1, self.range_size()) / 2

    def compute_range(self):
        low_value = max(0, self.get_range_center() - self.get_range_size())
        high_value = min(127, self.get_range_center() + self.get_range_size())
        if high_value < low_value + 1:
            high_value = low_value + 1
        return low_value, high_value

    def get_low_boundary(self):
        return self.compute_range()[0]

    def get_high_boundary(self):
        return self.compute_range()[1]

    def clear(self, *args):
        for subitem in [
            self.range_center,
            self.range_size,
            self.note_duration,
            self.velocity,
        ]:
            subitem.clear(*args)
