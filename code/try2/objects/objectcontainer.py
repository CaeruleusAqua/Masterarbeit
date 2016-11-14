import math

class ObjectContainer:
    def __init__(self):
        self.node_counter = 0
        self.lane_counter = 0
        self.nodes = list()
        self.lanes = list()
        self.surfaces = list()
        self.borders = list()

    def addNode(self, node):
        node.id = self.node_counter
        self.node_counter += 1
        self.nodes.append(node)

    def popLastNode(self):
        try:
            return self.nodes.pop()
        except IndexError:
            return None


    def addLane(self, lane):
        lane.id = self.lane_counter
        self.lane_counter += 1
        self.lanes.append(lane)

    def getNodeAt(self,x,y):
        for node in self.nodes:
            px,py = node.pos
            if math.sqrt((px-x)**2 + (py-y)**2) < 10:
                return node
        return None

    def getBorderAt(self,x,y):
        for border in self.borders:
            if border.dist_from_point((x,y)) < 10:
                return border
        return None
