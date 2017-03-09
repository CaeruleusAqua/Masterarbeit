#!/usr/bin/env python2
import pickle

import matplotlib.pyplot as plt
from rdp import rdp

from parser import Parser
from parser.Objects import *
import numpy as np
from tools import WGS84Coordinate

parser = Parser()

(lat, lon) = pickle.load(open("gps.p", "rb"))

roundabout_lon = 12.7751720037  # np.mean(lon[low_bound:upp_bound])
roundabout_lat = 57.772159681  # np.mean(lat[low_bound:upp_bound])

trans = WGS84Coordinate(57.772840, 12.769964)

points = list()
for i in xrange(12050, len(lat) - 1600):
    # for i in xrange(len(lat)):
    points.append(trans.transformToCart(lat[i], lon[i]))

# points.append([56.7924,0.27242])

circle0 = plt.Circle((0, 0), 15, color='b')
circle1 = plt.Circle((0, 0), 5, color='r')

fig, ax = plt.subplots()

#ax.add_artist(circle0)
#ax.add_artist(circle1)

fig.show()
q = list()
w = list()

points = rdp(points, epsilon=0.1)

for point in points:
    q.append(point[0])
    w.append(point[1])

roundabout = []

x,y = trans.transformToCart(roundabout_lat, roundabout_lon)
for deg in np.arange(0, 360, 2):
    w.append(np.cos(deg * trans.deg2rad) * 10 + y )
    q.append(np.sin(deg * trans.deg2rad) * 10 + x )
    roundabout.append([np.sin(deg * trans.deg2rad) * 10 + x , np.cos(deg * trans.deg2rad) * 10 + y ])

# parser.parseSCN("resources/scenario.scn")

scenario = parser.scenario
scenario.date = "December-10-2015"
scenario.ground.aerialimage = ScenarioImage()
scenario.ground.aerialimage.name = "AERIALIMAGE"
scenario.ground.aerialimage.file = "images/AstaZero-CityArea2.jpg"
scenario.ground.aerialimage.originx = 2570
scenario.ground.aerialimage.originy = 2502
scenario.ground.aerialimage.mppx = 0.128
scenario.ground.aerialimage.mppy = 0.128

scenario.ground.heightimage = ScenarioImage()
scenario.ground.heightimage.name = "HEIGHTIMAGE"
scenario.ground.heightimage.file = "images/HiQ_Elevation.jpg"
scenario.ground.heightimage.originx = 1080
scenario.ground.heightimage.originy = 476
scenario.ground.heightimage.mppx = 0.153
scenario.ground.heightimage.mppy = 0.153

scenario.origin = [57.772840, 12.769964]
scenario.addNewLayer("Groundfloor", 0.01)
scenario.layer[0].addNewRoad("driveway")
scenario.layer[0].roads[0].addNewLane(6, lanemarking_left=Lane.LaneMarking.SOLID_WHITE, lanemarking_right=Lane.LaneMarking.SOLID_WHITE)
scenario.layer[0].roads[0].lanes[0].pointmodel = points

scenario.layer[0].addNewRoad("roundabout")
scenario.layer[0].roads[1].addNewLane(6, lanemarking_left=Lane.LaneMarking.SOLID_WHITE, lanemarking_right=Lane.LaneMarking.SOLID_WHITE)
scenario.layer[0].roads[1].lanes[0].pointmodel = roundabout
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
            # lon = float(child.attrib['lon'])
            # lat = float(child.attrib['lat'])
            # x.append(gps.lon2x_m(lon))
            # y.append(gps.lat2y_m(lat))
        plt.plot(x, y, )
        x = list()
        y = list()

parser.saveSCN("resources/Scenarios/recording/scenario.scn")

#plt.plot(q, w, 'ro')
ax.set_aspect('equal', 'datalim')
plt.show()
