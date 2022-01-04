import mido


class MidiNotes:
    def __init__(self, port, channel):
        self.port = port
        self.channel = channel

    def send(self, msg):
        if not isinstance(msg, mido.Message):
            return
        msg.channel = self.channel
        self.port.send(msg)
