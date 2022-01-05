import json
from ..core.events import EventListener


class Scale(EventListener):
    def __init__(self, ec):
        self.ec = ec
        self.ec.subscribe("note_on", self.noteon)
        self.ec.subscribe("control_change", self.control_change)
        self.ec.subscribe("set_scale", self.on_set_scale)
        self.ec.subscribe("set_chord", self.on_set_chord)
        self.available_notes = []
        self.current_chord = []
        with open("orchestrator/master/scales.json", "r") as fp:
            self.available_scales = json.load(fp)
        with open("orchestrator/master/chords.json", "r") as fp:
            self.available_chords = json.load(fp)
        self.scale_name = "major"
        self.chord_name = "triad"
        self.degree = 0
        self.set_scale(self.scale_name, 60)
        self.set_chord(self.chord_name)
        super().__init__(ec)

    def transpose(self, root):
        oldroot = self.root
        self.root = root
        if oldroot is not None:
            transposition = oldroot - self.root
            self.available_notes = [
                note - transposition for note in self.available_notes
            ]

    def set_scale(self, scale_name="major", root=None):
        if root is not None:
            self.root = root
        self.scale_name = scale_name
        self.base_notes = [
            self.root + halftones
            for halftones in self.available_scales.get(scale_name, [0, 12])
        ]
        self.available_notes = self.base_notes[:]
        while self.available_notes[-1] < 127:
            self.available_notes += [
                n + 12 for n in self.available_notes[-(len(self.base_notes) - 1) :]
            ]
        while self.available_notes[0] > 0:
            self.available_notes = [
                n - 12 for n in self.available_notes[: (len(self.base_notes) - 1)]
            ] + self.available_notes
        self.available_notes = [n for n in self.available_notes if n >= 0 and n <= 127]
        self.ec.publish("display")

    def set_chord(self, chord_name="triad"):
        self.chord_name = chord_name
        self.current_chord = dict(self.available_chords)[self.chord_name]
        self.ec.publish("display")

    def on_set_scale(self, _evt, scale_name="major", root=None):
        self.set_scale(scale_name=scale_name, root=root)

    def on_set_chord(self, _evt, chord_name="triad"):
        self.set_chord(chord_name=chord_name)

    def noteon(self, event, msg):
        print(self._uimode)
        if self._uimode == "transpose":
            self.transpose(msg.note)
            self.ec.publish("uimode", None)

    def control_change(self, event, msg):
        if msg.channel != 15:
            return
        if msg.control >= 40 and msg.control <= 47 and msg.value == 127:
            chord_idx = msg.control - 40
            self.set_chord(self.available_chords[chord_idx][0])
        if msg.control == 33:
            self.change_degree(msg.value)
        if msg.control >= 48 and msg.control <= 55 and msg.value == 127:
            value = msg.control - 48
            degrees = len(self.base_notes)
            self.degree = int(value * degrees / 8)

    def change_degree(self, value):
        value = min(126, value)
        degrees = len(self.base_notes)
        self.degree = int(value * degrees / 127)
