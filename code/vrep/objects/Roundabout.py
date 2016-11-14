from VrepObject import VrepObject

class Roundabout(VrepObject):
    def __init__(self,clientID, name, lanes):
        self.lanes = lanes
        self.outer_r = 0
        for lane in lanes:
            if lane.outer_r > self.outer_r:
                self.outer_r = lane.outer_r

        super(Roundabout, self).__init__(clientID, name)
