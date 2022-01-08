import math
from ..numbers.value import Value as v


class BresenhamEuclideanRythm:
    def __init__(self, base=v(10), pulses=v(4), length=v(16)):
        self.base = base
        self.pulses = pulses
        self.length = length
        self.previous = None

    def __call__(self, step):
        if step % self.base() != 0:
            return
        x = (step / self.base()) % self.length()
        xprev = (x - 1) % self.length()
        # self.display(x)
        prev_value = int(math.floor(xprev * self.pulses() / self.length()))
        new_value = int(math.floor(x * self.pulses() / self.length()))
        return new_value != prev_value

    # def control_change(self, _event, msg):
    #     if msg.channel != 15:
    #         return
    #     if msg.control == 16:
    #         self.change_pulses(msg.value)
    #     if msg.control == 8:
    #         self.change_length(msg.value)

    # def change_pulses(self, value):
    #     self.pulses = int(value * 32 / 127)
    #     self.display()

    # def change_length(self, value):
    #     self.length = int(value * 32 / 127)
    #     self.display()

    def display(self, x=None):
        rythm = bresenham_euclidean_rythm(
            lambda x: x * self.pulses() / self.length(), self.length()
        )
        print("".join(map(lambda i: "x" if i else ".", rythm)))
        if x is not None:
            print("".join(["^" if x == idx else " " for idx, _ in enumerate(rythm)]))


class BresenhamCurveRythm:
    def __init__(self, output, base=v(10), curve=lambda x: x):
        self.output = output
        self.base = base
        self.curve = curve

    def __call__(self, step):
        if step % self.base() != 0:
            return
        prev_value = int(math.floor(self.curve((step - self.base()) / self.base())))
        new_value = int(math.floor(self.curve(step / self.base())))
        return new_value != prev_value


def bresenham_euclidean_rythm(func, pulses):
    result = []
    for x in range(pulses):
        previous = int(math.floor(func(x - 1)))
        y = int(math.floor(func(x)))
        result.append(1 if y != previous else 0)
    return result
