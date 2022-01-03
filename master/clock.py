
class Clock:
    def __init__(self, ec):
        self.ec = ec
        self.step = 0

    def clock(self, event, msg):
        self.step += 1
        self.ec.publish("tick", self.step)
