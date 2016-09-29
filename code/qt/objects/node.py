class Node:
    def __init__(self, pos):
        self.id = 0
        self.lanes = list()
        self.pos = (pos[0],pos[1])

    def connect(self, node, lane):
        self.lanes.append(lane)
        if lane.anchor is None:
            lane.anchor = self
        else:
            lane.nodes.append(self)
        lane.nodes.append(node)
