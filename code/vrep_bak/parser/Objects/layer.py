from road import Road
class Layer:
    def __init__(self):
        self.id = None
        self.name = None
        self.height = None
        self.roads = list()
        self.parent = None

        ## internal
        self.analyzed_id = False
        self.highest_id = 0


    def addNewRoad(self,name):
        road = Road()
        road.name = name
        road.parent = self
        road.id = self.getNextId()
        self.roads.append(road)


    def getNextId(self):
        if not self.analyzed_id:
            for road in self.roads:
                if road.id > self.highest_id:
                    self.highest_id = road.id
            self.analyzed_id = True

        self.highest_id += 1
        return self.highest_id
