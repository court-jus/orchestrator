import logging
import random

from ...events.listener import EventListener
from .value import Value

logger = logging.getLogger("RandomValue")


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
        logger.debug(
            f"Random between {vmin} and {vmax} (because {self.center()}, {self.size()})"
        )
        return random.randrange(vmin, vmax)

    def clear(self, *args):
        for subitem in [self.center, self.size]:
            subitem.clear(*args)
