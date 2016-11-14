from circle import Circle


class Car:
    def __init__(self, pos, color):
        self.acceleration = 0
        self.max_speed = 50
        self.speed = 0
        self.heading = 0
        self.pos = pos
        self.angle = 0
        self.size = [10, 20]
        self.circle = Circle(self.pos, 2, color, filled=True)

    def draw(self, surface, scale=1, offset=(0, 0)):
        self.circle.draw(surface, scale, offset)
