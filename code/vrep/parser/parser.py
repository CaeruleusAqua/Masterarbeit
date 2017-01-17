#!/usr/bin/env python2

import numpy as np

from Objects import GroundLayer
from Objects import Lane
from Objects import Layer
from Objects import Road
from Objects import Scenario
from Objects import ScenarioImage


class Parser:
    def __init__(self):
        self.scenario = Scenario()

    def layerLines(self, layer):
        endl = "\n"
        lines = "LAYER " + str(layer.name) + endl
        lines += "LAYERID " + str(layer.id) + endl
        lines += "HEIGHT " + str(layer.height) + endl
        for road in layer.roads:
            lines += self.roadLines(road)
        lines += "ENDLAYER" + endl

        return lines

    def roadLines(self, road):
        endl = "\n"
        lines = "ROAD" + endl
        lines += "ROADID " + str(road.id) + endl
        lines += "ROADNAME " + str(road.name) + endl
        for lane in road.lanes:
            lines += self.laneLines(lane)
        lines += "ENDROAD" + endl
        return lines

    def laneLines(self, lane):
        endl = "\n"
        lines = "LANE" + endl
        lines += "LANEID " + str(lane.id) + endl
        lines += "LANEWIDTH " + str(lane.width) + endl
        if lane.lanemarking_left is not None:
            lines += "LEFTLANEMARKING " + str(lane.lanemarking_left) + endl
        if lane.lanemarking_right is not None:
            lines += "RIGHTLANEMARKING " + str(lane.lanemarking_right) + endl

        # TODO connections
        for con in lane.connections:
            lines += "(1." + str(con[0][0].parent.id) + "." + str(con[0][0].id) + "." + str(con[0][1] + 1) + ")"
            lines += " -> "
            lines += "(1." + str(con[1][0].parent.id) + "." + str(con[1][0].id) + "." + str(con[1][1] + 1) + ")" + endl



            # (1.1.1.27) -> (1.2.1.1)

        lines += "POINTMODEL" + endl
        for id, vertex in enumerate(lane.pointmodel):
            if len(vertex) == 2:
                lines += "ID " + str(int(id + 1)) + endl
                lines += "VERTEX2" + endl
                lines += "X " + repr(vertex[0]) + endl
                lines += "Y " + repr(vertex[1]) + endl
            if len(vertex) == 3:
                lines += "ID " + str(int(id + 1)) + endl
                lines += "VERTEX3" + endl
                lines += "X " + repr(vertex[0]) + endl
                lines += "Y " + repr(vertex[1]) + endl
                lines += "Z " + repr(vertex[1]) + endl
        lines += "ENDPOINTMODEL" + endl
        lines += "ENDLANE" + endl

        return lines

    def saveSCN(self, file):
        with open(file, 'w') as f:
            endl = "\n"
            f.write("SCENARIO " + str(self.scenario.name) + endl)
            f.write("VERSION " + str(self.scenario.version) + endl)
            f.write("DATE " + str(self.scenario.date) + endl)
            f.write("ORIGINCOORDINATESYSTEM" + endl)
            f.write(str(self.scenario.coordinatesystem))
            f.write("ORIGIN" + endl)
            vertex = self.scenario.origin
            if len(vertex) == 2:
                f.write("VERTEX2" + endl)
                f.write("X " + repr(vertex[0]) + endl)
                f.write("Y " + repr(vertex[1]) + endl)
            if len(vertex) == 3:
                f.write("VERTEX3" + endl)
                f.write(repr(vertex[0]) + endl)
                f.write(repr(vertex[1]) + endl)
                f.write(repr(vertex[1]) + endl)
            f.write("ROTATION " + str(self.scenario.rotation) + endl)
            f.write("GROUND " + str(self.scenario.ground.name) + endl)
            f.write(self.scenario.ground.aerialimage.getLines())
            f.write(self.scenario.ground.heightimage.getLines())
            f.write("GROUNDHEIGHT " + str(self.scenario.ground.height) + endl)
            f.write("MINHEIGHT " + str(self.scenario.ground.minheight) + endl)
            f.write("MAXHEIGHT " + str(self.scenario.ground.maxheight) + endl)
            f.write("ENDGROUND" + endl)

            # TODO Add missing lines
            for layer in self.scenario.layer:
                f.write(self.layerLines(layer))
            f.write("ENDSCENARIO" + endl)

    def printSCN(self):
        for road in self.scenario.roads:
            print "ID: " + str(road.id) + " Name: " + str(road.name)
            for lane in road.lanes:
                print "    ID: " + str(lane.id) + " Width: " + str(lane.width)
                # print "        " + str(lane.pointmodel)

    def parseSCN(self, file):
        current_road = None
        current_lane = None
        current_object = None
        current_layer = None
        ground_layer = None
        x = None
        y = None
        z = None
        with open(file, 'r') as f:
            line = f.readline()
            while line:
                if line.startswith("SCENARIO "):
                    self.scenario.name = line.split(' ')[1].rstrip()

                elif line.startswith("VERSION "):
                    self.scenario.version = line.split(' ')[1].rstrip()

                elif line.startswith("DATE "):
                    self.scenario.date = line.split(' ')[1].rstrip()

                elif line.startswith("GROUND "):
                    ground_layer = GroundLayer()
                    self.scenario.ground = ground_layer
                    self.scenario.ground.name = line.split(' ')[1].rstrip()
                    while ground_layer is not None:
                        line = f.readline()
                        if line.startswith("AERIALIMAGE"):
                            image = ScenarioImage()
                            image.name = "AERIALIMAGE"
                            for i in xrange(6):
                                line = f.readline()
                                if line.startswith("IMAGE"):
                                    image.file = line.split(' ')[1].rstrip('\n')
                                elif line.startswith("ORIGINX"):
                                    image.originx = float(line.split(' ')[1])
                                elif line.startswith("ORIGINY"):
                                    image.originy = float(line.split(' ')[1])
                                elif line.startswith("MPPX"):
                                    image.mppx = float(line.split(' ')[1])
                                elif line.startswith("MPPY"):
                                    image.mppy = float(line.split(' ')[1])
                            self.scenario.ground.aerialimage = image




                        elif line.startswith("HEIGHTIMAGE"):
                            image = ScenarioImage()
                            image.name = "HEIGHTIMAGE"
                            for i in xrange(6):
                                line = f.readline()
                                if line.startswith("IMAGE"):
                                    image.file = line.split(' ')[1].rstrip('\n')
                                elif line.startswith("ORIGINX"):
                                    image.originx = float(line.split(' ')[1])
                                elif line.startswith("ORIGINY"):
                                    image.originy = float(line.split(' ')[1])
                                elif line.startswith("MPPX"):
                                    image.mppx = float(line.split(' ')[1])
                                elif line.startswith("MPPY"):
                                    image.mppy = float(line.split(' ')[1])
                            self.scenario.ground.heightimage = image

                        elif line.startswith("GROUNDHEIGHT"):
                            self.scenario.ground.height = float(line.split(' ')[1])

                        elif line.startswith("MINHEIGHT"):
                            self.scenario.ground.minheight = float(line.split(' ')[1])

                        elif line.startswith("MAXHEIGHT"):
                            self.scenario.ground.maxheight = float(line.split(' ')[1])

                        elif line.startswith("ENDGROUND"):
                            ground_layer = None



                elif line.startswith("ORIGINCOORDINATESYSTEM"):
                    line = f.readline()
                    self.scenario.coordinatesystem = line


                elif line.startswith("ORIGIN\n"):
                    line = f.readline()
                    if line.startswith("VERTEX2"):
                        x = float(f.readline().split(' ')[1])
                        y = float(f.readline().split(' ')[1])
                        self.scenario.origin = (x, y)
                    elif line.startswith("VERTEX3"):
                        x = float(f.readline().split(' ')[1])
                        y = float(f.readline().split(' ')[1])
                        z = float(f.readline().split(' ')[1])
                        self.scenario.origin = (x, y, z)
                    else:
                        print "Syntax Error"

                elif line.startswith("ROTATION"):
                    self.scenario.rotation = float(line.split(' ')[1])

                elif line.startswith("LAYER "):
                    current_layer = Layer()
                    current_layer.parent = self.scenario
                    current_layer.name = line.split(' ')[1].rstrip()

                elif line.startswith("HEIGHT "):
                    current_layer.height = float(line.split(' ')[1])

                elif line.startswith("LAYERID"):
                    current_layer.id = int(line.split(' ')[1])

                if line.startswith('ENDLAYER\n'):
                    self.scenario.layer.append(current_layer)
                    current_road = None


                elif line.startswith("ROAD\n"):
                    current_road = Road()
                    current_road.parent = current_layer
                    while current_road is not None:
                        line = f.readline()
                        if line.startswith('ENDROAD\n'):
                            current_layer.roads.append(current_road)
                            current_road = None

                        elif line.startswith('ROADID '):
                            current_road.id = int(line.split(' ')[1])

                        elif line.startswith('ROADNAME '):
                            current_road.name = line.split(' ')[1].rstrip()

                        elif line.startswith("LANE\n"):
                            current_lane = Lane()
                            current_lane.parent = current_road
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
                                    current_lane.lanemarking_left = (line.split(' ')[1]).rstrip()

                                elif line.startswith('RIGHTLANEMARKING '):
                                    current_lane.lanemarking_right = (line.split(' ')[1]).rstrip()

                                elif line.startswith('('):
                                    # current_lane.connections_str.append(line)
                                    current_lane.connections_str.append(line.replace("(", "").replace(")", "").replace(" ", "").replace("\n", ""))



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
                                            pointmodel.append((x, y, z))

                line = f.readline()

        ## connection s are defined as (layer.road.lane.vertex)
        for layer in self.scenario.layer:
            for road in layer.roads:
                for lane in road.lanes:
                    for conn in lane.connections_str:
                        [start, end] = conn.replace(">", "").split("-")
                        start = np.asarray(map(int, start.split("."))) - 1
                        end = np.asarray(map(int, end.split("."))) - 1
                        # print start
                        # print end
                        lane.connections.append(((lane, start[3]), (self.scenario.layer[end[0]].roads[end[1]].lanes[end[2]], end[3])))
