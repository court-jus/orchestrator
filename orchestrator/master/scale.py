import json
import logging

from ..events.listener import EventListener

logger = logging.getLogger("Scale")


class Scale(EventListener):
    def __init__(self, global_controller):
        self.inputdevice = None
        self.available_notes = []
        self.current_chord = []
        self.root = None
        # Idea: allow changing the root (or key) by following the circle of fifth:
        # C, G, D, A, E, B, F#, Db, Ab, Eb, Bb, F
        with open("orchestrator/master/scales.json", "r") as fp:
            self.available_scales = json.load(fp)
        with open("orchestrator/master/chords.json", "r") as fp:
            self.available_chords = json.load(fp)
        self.save_id = "global_scale"
        # Defaults
        self.scale_name = "gypsy min"
        self.chord_name = "7"
        self.root = 60
        self.degree = 0
        # Saved values
        if self.save_id in global_controller.loaded:
            saved = global_controller.loaded[self.save_id]
            self.scale_name = saved["scale"]
            self.chord_name = saved["chord"]
            self.degree = saved["degree"]
            self.root = saved["root"]
        super().__init__(global_controller.ec)
        if self.ec:
            self.set_event_channel(self.ec)

        self.set_scale(self.scale_name, self.root)
        self.set_chord(self.chord_name)
        global_controller.savables[self.save_id] = self

    def save(self):
        return {
            "scale": self.scale_name,
            "chord": self.chord_name,
            "degree": self.degree,
            "root": self.root,
        }

    def set_event_channel(self, ec):
        super().set_event_channel(ec)
        self.ec.subscribe("note_on", self.noteon)
        self.ec.subscribe("control_change", self.control_change)
        self.ec.subscribe("set_scale", self.on_set_scale)
        self.ec.subscribe("set_chord", self.on_set_chord)
        self.ec.subscribe("set_noteinput", self.set_noteinputdevice)
        self.ec.subscribe("set_degree", self.on_set_degree)

    def set_noteinputdevice(self, _event, msg, *a, **kw):
        self.inputdevice = msg

    def transpose(self, root):
        oldroot = self.root
        self.root = root
        if oldroot is not None:
            transposition = oldroot - self.root
            self.available_notes = [
                note - transposition for note in self.available_notes
            ]

    def set_scale(self, scale_name="ionian - major", root=None):
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
        logger.debug(f"New scale {self.scale_name}")

    def set_chord(self, chord_name="triad"):
        self.chord_name = chord_name
        self.current_chord = dict(self.available_chords)[self.chord_name]
        self.ec.publish("display")
        logger.debug(f"New chord {self.chord_name}")

    def set_degree(self, degree=0):
        self.degree = degree
        self.ec.publish("display")
        logger.info(f"New chord degree {self.degree}")

    def on_set_scale(self, _evt, scale_name="ionian - major", root=None, *_a, **_kw):
        self.set_scale(scale_name=scale_name, root=root)

    def on_set_chord(self, _evt, chord_name="triad", *_a, **_kw):
        self.set_chord(chord_name=chord_name)

    def on_set_degree(self, _event, degree=0):
        self.set_degree(degree=degree)

    def noteon(self, _event, msg, *_a, **kw):
        if self._uimode == "transpose" and kw.get("midi_port_name") == self.inputdevice:
            self.transpose(msg.note)
            self.ec.publish("display")
            self.ec.publish("uimode", None)

    def control_change(self, _event, msg, *_a, **_kw):
        if msg.channel != 15:
            return
        if msg.control >= 40 and msg.control <= 47 and msg.value == 127:
            chord_idx = msg.control - 40
            self.set_chord(self.available_chords[chord_idx][0])
        if msg.control >= 48 and msg.control <= 55 and msg.value == 127:
            value = msg.control - 48
            degrees = len(self.base_notes)
            self.set_degree(int(value * degrees / 8))
