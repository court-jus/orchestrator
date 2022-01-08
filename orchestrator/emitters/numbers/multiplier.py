from .value import Value


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
        multiplier = orange / irange
        return ((self.value() - self.imin()) * multiplier) + self.omin()
