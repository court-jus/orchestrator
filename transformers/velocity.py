import random


class VelocityTransformer:
    def __init__(self, output, min=0, max=127):
        self.output = output
        self.min = min
        self.max = max

    def send(self, input_msg):
        if input_msg.type != "note_on":
            self.output.send(input_msg)
            return

        input_msg.velocity = random.randrange(self.min, self.max)
        self.output.send(input_msg)
