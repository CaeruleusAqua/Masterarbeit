import cv2


class Circle:
    def __init__(self, pos, radius, color, filled=False):
        self.pos = pos
        self.radius = radius
        self.color = color
        if not filled:
            self.thickness = 1
        else:
            self.thickness = -1

    def draw(self, surface, scale=1, offset=(0, 0)):
        cv2.circle(surface, (int(self.pos[0] * scale + offset[0]), int(self.pos[1] * scale + offset[1])), int(self.radius * scale), self.color, self.thickness)
