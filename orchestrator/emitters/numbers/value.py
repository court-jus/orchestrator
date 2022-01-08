class Value:
    def __init__(self, generator):
        self.generator = generator

    def __call__(self):
        return self.generator
