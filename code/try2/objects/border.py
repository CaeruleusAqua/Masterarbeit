from math import *


class Border:
    def __init__(self, a, b):
        self.id = 0
        self.type = "fixed"
        self.node_a = a
        self.node_b = b
        self.node_a.parents.append(self)
        self.node_b.parents.append(self)
        self.parents = list()

    def dist_from_point(self, pos):
        x0, y0 = pos
        x1, y1 = self.node_a.pos
        x2, y2 = self.node_b.pos
        z = abs((y2 - y1) * x0 - (x2 - x1) * y0 + x2 * y1 - y2 * x1)
        n = sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)
        return z / float(n)

    def update(self):
        for parent in self.parents:
            parent.update()
