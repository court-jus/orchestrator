import mido
import math

from .events import EventListener
from .values import Value

v = Value


class LFO(EventListener, Value):
    def __init__(self, ec, min=v(0), max=v(127), rate=v(1), shape="sin"):
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

    def tick(self, _evt, step):
        value = getattr(LFO, self.shape)(step / self.rate())
        self.value = int((value * (self.max() - self.min()) / 127) + self.min())
        # print("LFO value", self.value, step, step / self.rate)

    @staticmethod
    def sin(value):
        return (math.sin(value) + 1) * 64
