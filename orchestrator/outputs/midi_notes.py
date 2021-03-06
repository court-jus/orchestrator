import logging

import mido

from ..emitters import Value
from ..master.controller import global_controller
from ..tools.midi import get_port

logger = logging.getLogger("MidiNotes")


class MidiNotes:
    def __init__(self, port, channel, duration=Value(3), velocity=Value(60)):
        self.port = get_port(port) if isinstance(port, str) else port
        self.channel = channel
        self.msg_buffer = {}  # Note -> (stopat, msg_off)
        self.duration = duration
        self.velocity = velocity
        global_controller.ec.subscribe("tick", self.tick)

    def tick(self, event, step, *_a, **_kw):
        stopped = []
        for note, (stopat, msg_off) in self.msg_buffer.items():
            if stopat == step:
                if self.port:
                    logger.debug(msg_off)
                    self.port.send(msg_off)
                stopped.append(note)
        for n in stopped:
            self.msg_buffer.pop(n)

    def __call__(self, msg):
        if isinstance(msg, list):
            for item in msg:
                self.__call__(item)
            return

        if isinstance(msg, int):
            msg = mido.Message(
                "note_on", channel=self.channel, note=msg, velocity=self.velocity()
            )

        if not isinstance(msg, mido.Message):
            return

        if msg.type == "note_on":
            # Stop note if already playing
            msg_off = self.msg_buffer.pop(msg.note, None)
            if msg_off and self.port:
                logger.debug(msg_off[1])
                self.port.send(msg_off[1])

            # Play and store off message
            stopat = global_controller.clock.step + self.duration()
            msg_dict = msg.dict()
            msg_dict["type"] = "note_off"
            self.msg_buffer[msg.note] = (stopat, mido.Message.from_dict(msg_dict))

        if self.port:
            msg.channel = self.channel
            logger.debug(msg)
            self.port.send(msg)

    def clear(self, *args):
        for subitem in [self.duration, self.velocity]:
            subitem.clear(*args)
        global_controller.ec.unsubscribe_all(self)

    def close(self):
        if self.port:
            self.port.close()
