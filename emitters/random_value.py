import random
from ..events.listener import EventListener
from .value import Value


class RandomValue(Value):
    def __init__(self, min=Value(0), max=Value(127)):
        self.min = min
        self.max = max
        self.value = random.randrange(self.min(), self.max())

    def __call__(self):
        self.value = random.randrange(self.min(), self.max())
        return self.value
