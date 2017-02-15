from lane import Lane


class Road:
    def __init__(self):
        self.id = None
        self.name = None
        self.lanes = list()
        self.parent = None

        ## internal
        self.analyzed_id = False
        self.highest_id = 0

    def addNewLane(self, width, lanemarking_right=None, lanemarking_left=None):
        lane = Lane()
        lane.parent = self
        lane.width = width
        if lanemarking_left is not None:
            lane.lanemarking_left = lanemarking_left
        if lanemarking_right is not None:
            lane.lanemarking_right = lanemarking_right


        lane.id = self.getNextId()
        self.lanes.append(lane)

    def getNextId(self):
        if not self.analyzed_id:
            for lane in self.lanes:
                if lane.id > self.highest_id:
                    self.highest_id = lane.id
            self.analyzed_id = True

        self.highest_id += 1
        return self.highest_id
