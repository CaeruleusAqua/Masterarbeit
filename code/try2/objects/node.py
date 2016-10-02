class Node:
    def __init__(self, pos):
        self.id = 0
        self.lanes = list()
        self.nodes = list()
        self.pos = [pos[0], pos[1]]
        self.border = list()
        self.type = "Node"

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

    def action(self):
        pass






