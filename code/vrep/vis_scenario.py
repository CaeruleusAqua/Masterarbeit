#!/usr/bin/env python2
import matplotlib.pyplot as plt

from parser import Parser

fig = plt.figure()

parser = Parser()
parser.parseSCN("resources/scenario.scn")
scenario = parser.scenario

x = list()
y = list()

i = 0
for road in scenario.layer[0].roads:
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

# plt.plot(x, y, 'ro')
plt.axes().set_aspect('equal', 'datalim')

plt.show()
