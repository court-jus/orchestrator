from ..core.events import EventListener


class Scale(EventListener):
    def __init__(self, ec):
        self.ec = ec
        self.ec.subscribe("note_on", self.noteon)
        self.ec.subscribe("set_scale", self.on_set_scale)
        self.available_notes = []
        self.root = None
        super().__init__(ec)

    def set_root(self, root):
        oldroot = self.root
        self.root = root
        if oldroot is not None:
            transposition = oldroot - self.root
            self.available_notes = [
                note - transposition for note in self.available_notes
            ]

    def set_scale(self, scale_type="major", root=None):
        if root is not None:
            self.root = root
        if self.root is None:
            self.root = 60
        self.base_notes = [
            self.root + halftones
            for halftones in {
                "major": [0, 2, 4, 5, 7, 9, 11, 12],
                "minor": [0, 2, 3, 5, 7, 9, 10, 12],
            }.get(scale_type, [0, 12])
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

    def on_set_scale(self, _evt, scale_type="major", root=None):
        self.set_scale(scale_type=scale_type, root=root)

    def noteon(self, event, msg):
        print(self._uimode)
        if self._uimode == "set_root":
            self.set_root(msg.note)
            self.ec.publish("uimode", None)
        print(self.root)
        print(self.available_notes)
