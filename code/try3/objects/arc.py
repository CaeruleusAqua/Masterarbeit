import cv2


class Arc:
    def __init__(self, pos, radius, color, startAngle, endAngle, filled=False):
        self.pos = pos
        self.radius = radius
        self.color = color
        self.startAngle = startAngle
        self.endAngle = endAngle

        if not filled:
            self.thickness = 1
        else:
            self.thickness = -1
        self.angle = 0

    def draw(self, surface, scale=1, offset=(0, 0)):
        cv2.ellipse(surface, (int(self.pos[0] * scale + offset[0]), int(self.pos[1] * scale + offset[1])), (
            int(self.radius * scale), int(self.radius * scale)), angle=self.angle, startAngle=self.startAngle, endAngle=self.endAngle, color=self.color,
                    thickness=self.thickness)