import math
import numpy as np
from math import cos, sin

from ark import Ark
from junction import Junction


class Roundabout:
    def __init__(self, pos):
        self.pos = np.array(pos)
        self.junctions = dict()

    def add_junktion(self, angle, radius):
        junc = Junction(self.pos + [radius * cos(angle), radius * sin(angle)])
        self.junctions[angle] = junc

    def chain(self):
        keys = sorted(self.junctions.keys(), reverse=True)
        print keys
        for i in xrange(len(keys) - 1):
            self.junctions[keys[i]].connect(self.junctions[keys[i + 1]], Ark(radius=20,start=keys[i+1],end=keys[i],center=self.pos))
            print "con: " + str(i) + " + " + str(i + 1)
        # self.junctions[keys[0]].connect(self.junctions[keys[-1]], Ark(radius=10,start=keys[0],end=keys[-1]))
        self.junctions[keys[0]].connect(self.junctions[keys[-1]], Ark(radius=20,start=keys[0],end=keys[-1]+2*math.pi,center=self.pos))
