#!/usr/bin/env python

from parser.Objects import Lane
from parser.Objects import Road
from parser.Objects import Scenario
import matplotlib.pyplot as plt

roads = list()
current_road = None
current_lane = None
current_object = None
scenario = Scenario()

x = None
y = None
z = None

with open('resources/scenario.scn', 'r') as f:
    line = f.readline()
    while line:
        if line.startswith("SCENARIO "):
            scenario.name = line.split(' ')[1]

        elif line.startswith("VERSION "):
            scenario.version = line.split(' ')[1]

        elif line.startswith("DATE "):
            scenario.date = line.split(' ')[1]

        elif line.startswith("ORIGINCOORDINATESYSTEM"):
            line = f.readline()
            scenario.coordinatesystem = line

        elif line.startswith("ORIGIN\n"):
            line = f.readline()
            if line.startswith("VERTEX2"):
                x = float(f.readline().split(' ')[1])
                y = float(f.readline().split(' ')[1])
            elif line.startswith("VERTEX3"):
                x = float(f.readline().split(' ')[1])
                y = float(f.readline().split(' ')[1])
                z = float(f.readline().split(' ')[1])
            else:
                print "Syntax Error"

        elif line.startswith("ROAD\n"):
            current_road = Road()
            while current_road is not None:
                line = f.readline()
                if line.startswith('ENDROAD\n'):
                    scenario.roads.append(current_road)
                    current_road = None

                elif line.startswith('ROADID '):
                    current_road.id = int(line.split(' ')[1])

                elif line.startswith('ROADNAME '):
                    current_road.name = line.split(' ')[1]

                elif line.startswith("LANE\n"):
                    current_lane = Lane()
                    while current_lane is not None:
                        line = f.readline()
                        if line.startswith('ENDLANE\n'):
                            current_road.lanes.append(current_lane)
                            current_lane = None

                        elif line.startswith('LANEID '):
                            current_lane.id = int(line.split(' ')[1])

                        elif line.startswith('LANEWIDTH '):
                            current_lane.width = float(line.split(' ')[1])

                        elif line.startswith('LEFTLANEMARKING '):
                            current_lane.lanemarking_left = (line.split(' ')[1])

                        elif line.startswith('RIGHTLANEMARKING '):
                            current_lane.lanemarking_right = (line.split(' ')[1])

                        elif line.startswith("POINTMODEL\n"):
                            pointmodel = list()
                            while pointmodel is not None:
                                line = f.readline()
                                if line.startswith('ENDPOINTMODEL\n'):
                                    current_lane.pointmodel = pointmodel
                                    pointmodel = None
                                elif line.startswith("VERTEX2"):
                                    x = float(f.readline().split(' ')[1])
                                    y = float(f.readline().split(' ')[1])
                                    pointmodel.append((x, y))
                                elif line.startswith("VERTEX3"):
                                    x = float(f.readline().split(' ')[1])
                                    y = float(f.readline().split(' ')[1])
                                    z = float(f.readline().split(' ')[1])
                                    pointmodel.append(x, y, z)

        line = f.readline()


for road in scenario.roads:
    print "ID: " + str(road.id)  + " Name: " + str(road.name)
    for lane in road.lanes:
        print "    ID: " + str(lane.id) + " Width: " + str(lane.width)
        print "        " + str(lane.pointmodel)
        for point in lane.pointmodel:
            plt.plot(point[0],point[1], 'ro')

plt.axes().set_aspect('equal', 'datalim')
plt.show()
