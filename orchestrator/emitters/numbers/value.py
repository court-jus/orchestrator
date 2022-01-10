class Value:
    def __init__(self, value):
        self.value = value

    def __call__(self):
        return self.value
