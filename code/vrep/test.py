#!/usr/bin/env python2
#from parser import Parser
from parser.Objects.line import LineSegment

import numpy as np


#parser = Parser()
#parser.parseSCN("resources/scenario.scn")
#parser.saveSCN("resources/scenario_new.scn")

test=LineSegment(np.array([0,0]),np.array([10,0]),4)

print test.distance
print test.normal
print test.getDist(np.array([2,2]))



print test.isInSegment(np.array([0,2]))