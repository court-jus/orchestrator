import random
from ...events.listener import EventListener
from .value import Value


class RandomValue(Value):
    def __init__(self, center=Value(64), size=Value(12)):
        self.center = center
        self.size = size
        self.value = self.compute()

    def __call__(self):
        self.value = self.compute()
        return self.value

    def compute(self):
        vmin = int(self.center() - self.size())
        vmax = int(self.center() + self.size())
        return random.randrange(vmin, vmax)
