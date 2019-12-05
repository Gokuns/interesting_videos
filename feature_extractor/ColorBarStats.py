class ColorBarStats:
    maximum = 0
    minimum = 0
    average = 0.0

    def __init__(self, maximum: float, minimum: float, average: float):
        self.average = average
        self.maximum = maximum
        self.minimum = minimum

    # def get_color(self, ):