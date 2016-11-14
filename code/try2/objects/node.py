class Node:
    def __init__(self, pos):
        self.id = 0
        self.lanes = list()
        self.nodes = list()
        self.pos = [pos[0], pos[1]]
        self.border = list()
        self.type = "Node"
        self.parents = list()
        self.movable = True

    def connect(self, node, lane):
        self.lanes.append(lane)
        if lane.anchor is None:
            lane.anchor = self
        else:
            lane.nodes.append(self)
        lane.nodes.append(node)
        self.nodes.append(node)

    def connected_to(self, node):
        return node in self.nodes

    def setPos(self,pos):
        self.pos = [pos[0], pos[1]]
        self.update()

    def update(self):
        for parent in self.parents:
            parent.update()

