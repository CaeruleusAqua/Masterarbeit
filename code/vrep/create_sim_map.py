#!/usr/bin/env python2

import matplotlib.pyplot as plt
import numpy as np

from parser import Parser
from parser.Objects import *
from tools import WGS84Coordinate

parser = Parser()

fig, ax = plt.subplots()

fig.show()

points_car = list()
points_bicycle = list()
points_ped = list()
trans = WGS84Coordinate(57.772840, 12.769964)

for deg in np.arange(0, 360, 5):
    points_car.append([np.cos(deg * trans.deg2rad) * 11, np.sin(deg * trans.deg2rad) * 11])
    points_bicycle.append([np.cos(deg * trans.deg2rad) * 20.85, np.sin(deg * trans.deg2rad) * 20.85])
    points_ped.append([np.cos(deg * trans.deg2rad) * 22.85, np.sin(deg * trans.deg2rad) * 22.85])

# parser.parseSCN("resources/scenario.scn")

scenario = parser.scenario
scenario.date = "December-10-2015"
scenario.ground.aerialimage = ScenarioImage()
scenario.ground.aerialimage.name = "AERIALIMAGE"
scenario.ground.aerialimage.file = "images/minikreisverkehr.jpg"
scenario.ground.aerialimage.originx = 1024
scenario.ground.aerialimage.originy = 1024
scenario.ground.aerialimage.mppx = 0.048828125
scenario.ground.aerialimage.mppy = 0.048828125

scenario.ground.heightimage = ScenarioImage()
scenario.ground.heightimage.name = "HEIGHTIMAGE"
scenario.ground.heightimage.file = "images/HiQ_Elevation.jpg"
scenario.ground.heightimage.originx = 1080
scenario.ground.heightimage.originy = 476
scenario.ground.heightimage.mppx = 0.153
scenario.ground.heightimage.mppy = 0.153

scenario.origin = [57.772840, 12.769964]
scenario.addNewLayer("Groundfloor", 0.01)

# Add Roundabout
scenario.layer[0].addNewRoad("Roundabout")
scenario.layer[0].roads[0].addNewLane(8, lanemarking_left=Lane.LaneMarking.SOLID_WHITE, lanemarking_right=Lane.LaneMarking.SOLID_WHITE)
scenario.layer[0].roads[0].lanes[0].pointmodel = points_car
scenario.layer[0].roads[0].addNewLane(1.85, lanemarking_left=Lane.LaneMarking.SOLID_WHITE, lanemarking_right=Lane.LaneMarking.SOLID_WHITE)
scenario.layer[0].roads[0].lanes[1].pointmodel = points_bicycle
scenario.layer[0].roads[0].addNewLane(2, lanemarking_left=Lane.LaneMarking.SOLID_WHITE, lanemarking_right=Lane.LaneMarking.SOLID_WHITE)
scenario.layer[0].roads[0].lanes[2].pointmodel = points_ped

##Add streets
scenario.layer[0].addNewRoad("West")
scenario.layer[0].roads[1].addNewLane(6, lanemarking_left=Lane.LaneMarking.SOLID_WHITE, lanemarking_right=Lane.LaneMarking.SOLID_WHITE)
scenario.layer[0].roads[1].lanes[0].pointmodel = [[-50, 0], [-15, 0]]
scenario.layer[0].addNewRoad("East")
scenario.layer[0].roads[2].addNewLane(6, lanemarking_left=Lane.LaneMarking.SOLID_WHITE, lanemarking_right=Lane.LaneMarking.SOLID_WHITE)
scenario.layer[0].roads[2].lanes[0].pointmodel = [[50, 0], [15, 0]]
scenario.layer[0].addNewRoad("North")
scenario.layer[0].roads[3].addNewLane(4, lanemarking_left=Lane.LaneMarking.SOLID_WHITE, lanemarking_right=Lane.LaneMarking.SOLID_WHITE)
scenario.layer[0].roads[3].lanes[0].pointmodel = [[2, 50], [2, 20]]
scenario.layer[0].roads[3].addNewLane(4, lanemarking_left=Lane.LaneMarking.SOLID_WHITE, lanemarking_right=Lane.LaneMarking.SOLID_WHITE)
scenario.layer[0].roads[3].lanes[1].pointmodel = [[-2, 50], [-2, 20]]
scenario.layer[0].addNewRoad("South")
scenario.layer[0].roads[4].addNewLane(4, lanemarking_left=Lane.LaneMarking.SOLID_WHITE, lanemarking_right=Lane.LaneMarking.SOLID_WHITE)
scenario.layer[0].roads[4].lanes[0].pointmodel = [[-2, -50], [-2, -20]]
scenario.layer[0].roads[4].addNewLane(4, lanemarking_left=Lane.LaneMarking.SOLID_WHITE, lanemarking_right=Lane.LaneMarking.SOLID_WHITE)
scenario.layer[0].roads[4].lanes[1].pointmodel = [[2, -50], [2, -20]]



parser.scenario = scenario
print scenario.layer[0].name

x = list()
y = list()

for road in parser.scenario.layer[0].roads:
    print road.name, road.id
    for lane in road.lanes:
        for point in lane.pointmodel:
            x.append(point[0])
            y.append(point[1])

        plt.plot(x, y, )
        x = list()
        y = list()

parser.saveSCN("resources/Scenarios/scenario.scn")

ax.set_aspect('equal', 'datalim')
plt.show()
