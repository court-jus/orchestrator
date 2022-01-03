class Scale:
    def __init__(self):
        self.available_notes = []
        self.root = None

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
        self.available_notes = [
            self.root + halftones
            for halftones in {
                "major": [0, 2, 4, 5, 7, 9, 11, 12],
                "minor": [0, 2, 3, 5, 7, 9, 10, 12],
            }.get(scale_type, [0, 12])
        ]

    def noteon(self, event, msg):
        self.set_root(msg.note)
        print(self.root)
        print(self.available_notes)
