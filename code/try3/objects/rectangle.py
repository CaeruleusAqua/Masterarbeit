import cv2


class Rectangle:
    def __init__(self, pos, radius, color):
        self.x = pos[0]
        self.y = pos[1]
        self.radius = radius
        self.color = color
        self.angle = 0

    def draw(self, surface):
        # TODO
        cv2.circle(surface, (self.x, self.x), self.radius, self.color)
