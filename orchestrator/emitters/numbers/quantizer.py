from .. import Value


def extend_list(in_list):
    result = []
    for x in range(128):
        for y in in_list:
            if (x - y) % 12 == 0:
                result.append(x)
                break
    return result


class Quantizer(Value):
    def __init__(
        self,
        value=Value(0),
        to=Value([0, 1]),
        filter_in=Value(True),
        extend=Value(True),
    ):
        self.value = value
        self.quantize_to = to
        self.filter_in = filter_in
        self.extend = extend

    def __call__(self):
        available = sorted(self.quantize_to())
        v = self.value()

        if v is None:
            return None

        if self.extend():
            available = extend_list(available)

        if v in available:
            return v

        if self.filter_in():
            return None

        # Find the available value that is the closest to v
        deltas = sorted([v - n for n in available], key=abs)
        return int(v - deltas[0])

    def clear(self, *args):
        for subitem in [self.value, self.quantize_to, self.filter_in, self.extend]:
            subitem.clear(*args)
