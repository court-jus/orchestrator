import logging

from .value import Value

logger = logging.getLogger("Multiplier")


class Multiplier(Value):
    def __init__(
        self,
        value=Value(0),
        imin=Value(0),
        imax=Value(127),
        omin=Value(0),
        omax=Value(127),
    ):
        self.imin = imin
        self.imax = imax
        self.omin = omin
        self.omax = omax
        self.value = value

    def __call__(self):
        irange = self.imax() - self.imin()
        orange = self.omax() - self.omin()
        logger.debug(f"IRANGE = {irange} ({self.imax()} - {self.imin()})")
        logger.debug(f"ORANGE = {orange} ({self.omax()} - {self.omin()})")
        multiplier = orange / irange
        multiplied = ((self.value() - self.imin()) * multiplier) + self.omin()
        logger.debug(
            f"MULTIPLIER = {multiplier}, VALUE = {self.value()}, MULTIPLIED = {multiplied}"
        )
        return multiplied

    def clear(self, *args):
        for subitem in [self.value, self.imin, self.imax, self.omin, self.omax]:
            subitem.clear(*args)
