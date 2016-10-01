from node import Node


class Surface:
    def __init__(self, nodes):
        self.id = 0
        assert len(nodes) == 4
        self.nodes = nodes

        x = 0
        y = 0
        for node in self.nodes:
            x += node.pos[0]
            y += node.pos[1]
        x /= 4
        y /= 4
        self.ancher = Node([x, y])

    def getAnchor(self):
        return self.ancher
