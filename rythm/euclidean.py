import math
from ..core import EventListener, LFO
from ..core.values import Value as v


class BresenhamEuclideanRythm(EventListener):
    def __init__(self, ec, output, base=v(10), pulses=v(4), length=v(16)):
        ec.subscribe("tick", self.tick)
        ec.subscribe("control_change", self.control_change)
        self.output = output
        self.base = base
        self.pulses = pulses
        self.length = length
        self.previous = None

    def tick(self, _event, step):
        if step % self.base() != 0:
            return
        # self.display()
        new_value = int(math.floor(step / self.base() * self.pulses() / self.length()))
        if new_value != self.previous:
            self.output.send(step)
        else:
            self.output.send(0)
        self.previous = new_value

    def control_change(self, _event, msg):
        if msg.channel != 15:
            return
        if msg.control == 16:
            self.change_pulses(msg.value)
        if msg.control == 8:
            self.change_length(msg.value)

    def change_pulses(self, value):
        self.pulses = int(value * 32 / 127)
        self.display()

    def change_length(self, value):
        self.length = int(value * 32 / 127)
        self.display()

    def display(self):
        rythm = bresenham_euclidean_rythm(
            lambda x: x * self.pulses() / self.length(), self.length()
        )
        print("".join(map(lambda i: "x" if i else ".", rythm)))


class BresenhamCurveRythm(EventListener):
    def __init__(self, output, base=v(10), curve=lambda x: x):
        self.output = output
        self.base = base
        self.curve = curve
        self.previous = None

    def tick(self, _event, step):
        if step % self.base() != 0:
            return
        new_value = int(math.floor(self.curve(step / self.base())))
        if new_value != self.previous:
            self.output.send(step)
        else:
            self.output.send(0)
        self.previous = new_value


def bresenham_euclidean_rythm(func, pulses):
    result = []
    previous = None
    for x in range(pulses):
        y = int(math.floor(func(x)))
        result.append(1 if y != previous else 0)
        previous = y
    return result


# def to_str(i):
#     return "x" if i else "."


# def display(rythm):
#     print("".join(map(to_str, rythm)))


# display(bresenham_euclidean_rythm(lambda x: 2 * math.sin(x), 40))
# display(bresenham_euclidean_rythm(lambda x: x * 5 / 13, 40))
