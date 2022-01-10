import logging
import math

from ...events.listener import EventListener
from .value import Value

logger = logging.getLogger("LFO")


class LFO(EventListener, Value):
    def __init__(self, ec, min=Value(0), max=Value(127), rate=Value(1), shape="sin"):
        self.value = 0
        self.min = min
        self.max = max
        self.rate = rate
        self.shape = shape
        super().__init__(ec)
        if self.ec:
            ec.subscribe("tick", self.tick)

    def __call__(self):
        return self.value

    def tick(self, _event, step):
        value = getattr(LFO, self.shape)(step / self.rate())
        self.value = int((value * (self.max() - self.min()) / 127) + self.min())
        if self.ec.debug:
            logger.debug(
                f"LFO value: {self.value} (at step {step} => {step / self.rate()})"
            )

    @staticmethod
    def sin(value):
        return (math.sin(value) + 1) * 64

    def clear(self, *args):
        for subitem in [self.min, self.max, self.rate]:
            subitem.clear(*args)
        self.ec.unsubscribe_all(self)
