from ...master.controller import global_controller


class ChordsEmitter:
    def __call__(self):
        return self.get_notes()

    def get_notes(self):
        scale_notes = sorted(global_controller.scale.available_notes)
        root_note_index = scale_notes.index(global_controller.scale.root)
        notes = [
            scale_notes[root_note_index + global_controller.scale.degree + degree]
            for degree in global_controller.scale.current_chord
        ]
        return [
            scale_notes[root_note_index + global_controller.scale.degree + degree]
            for degree in global_controller.scale.current_chord
        ]
