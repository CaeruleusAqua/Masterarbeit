import pygame
import numpy as np

class Junction:
    def __init__(self, pos):
        self.lanes = list()
        self.pos = np.array(pos)


    def connect(self, junction, lane, type="oneway"):
        if type == "oneway":
            self.lanes.append(lane)
            lane.junctions.append(junction)
            lane.junctions.append(self)
        elif type == "twoway":
            self.lanes.append(lane)
            lane.junctions.append(junction)
            lane.junctions.append(self)
            junction.lanes.append(lane)
        else:
            raise NotImplementedError("Lanetype \'" + type + "\' is not implemented")
