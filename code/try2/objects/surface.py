from node import Node


class Surface:
    def __init__(self, borders):
        self.id = 0
        assert len(borders) == 4
        self.borders = borders
        self.anchor = Node([0, 0])
        for border in borders:
            border.parents.append(self)
        self.update()

    def getAnchor(self):
        return self.anchor

    def update(self):
        x = 0
        y = 0
        for border in self.borders:
            x += border.node_a.pos[0]
            y += border.node_a.pos[1]
        x /= 4
        y /= 4
        self.anchor.setPos([x, y])
        self.anchor.movable = False
