import datetime
from layer import Layer
from groundlayer import GroundLayer


class Scenario:
    def __init__(self):
        self.version = "v1.0"
        self.date = datetime.datetime.now()
        self.coordinatesystem = "WGS84"
        self.name = "Masterarbeit"
        self.origin = []
        self.ground = GroundLayer()
        self.ground.parent = self
        self.rotation = 0
        self.layer = list()

        ## internal

        self.analyzed_id = False
        self.highest_id = 0

    def addNewLayer(self, name, height):
        layer = Layer()
        layer.name = name
        layer.height = height
        layer.parent = self
        layer.id = self.getNextId()
        self.layer.append(layer)
        print "ID = " + str(layer.id)

    def getNextId(self):
        if not self.analyzed_id:
            for layer in self.layer:
                if layer.id > self.highest_id:
                    self.highest_id = layer.id
            self.analyzed_id = True

        self.highest_id += 1

        return self.highest_id

    def getLineSegments(self, pos):
        possible_objects = list()
        for road in self.layer[0].roads:
            for lane in road.lanes:
                for segment in lane.lineSegments:
                    distance = segment.isInSegment(pos)
                    if distance is not False:
                        possible_objects.append([segment,distance])
        return possible_objects

    def getDistance(self, startSegment, endSegment):
        print "Start Index: ", startSegment.index
        print "End Index: ", endSegment.index
        if startSegment.index >= endSegment.index:
            current_segment = startSegment
            length = 0
            while current_segment.index != endSegment.index:
                length += current_segment.length
                current_segment = current_segment.successor

            return length

        else:
            current_segment = endSegment
            length = 0
            while current_segment.index != startSegment.index:
                length += current_segment.length
                current_segment = current_segment.precursor

            return length
