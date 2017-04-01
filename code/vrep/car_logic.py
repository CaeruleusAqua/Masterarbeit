#!/usr/bin/env python2

import math
import time

import numpy as np

import States
from Objects import Enemy
from Objects import DetectionEnemy
from Objects import Lane
from Objects import Roundabout
from Objects import VrepObject
from remoteApi import vrep
from remoteApi import vrepConst
from parser import Parser
import matplotlib.pyplot as plt
import struct

import pickle

from opendavinci.DVnode import DVnode
import cv2
from tools import WGS84Coordinate

import socket


class CarLogic:
    def __init__(self, port):
        TCP_IP = '127.0.0.1'
        TCP_PORT = 1234
        self.BUFFER_SIZE = 98  # Normally 1024, but we want fast response

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((TCP_IP, TCP_PORT))
        s.listen(1)

        self.conn, self.addr = s.accept()

        self.clientID = -1
        self.port = port
        self.parser = Parser()
        self.parser.parseSCN("resources/Scenarios/simulation_2/scenario.scn")
        self.trans = WGS84Coordinate(57.772840, 12.769964)
        self.milliseconds = 0
        self.seconds = 0
        self.minutes = 0

        # Parameters:
        self.time = time.time()
        self.speed = 0.33
        self.target_speed = 0.83
        self.max_speed = 0.83
        self.length = 0
        self.dt = 0.05
        self.accel = 0.3
        self.neg_accel = 0.4
        self.max_dist = 30
        self.speed_array = list()
        self.alpha_array = list()
        self.b = list()
        self.car_length = 0.5
        self.max_neg_accel = 1.1
        self.first = True

        self.handleBuffer = []

        self.currentState = States.Start(self)
        self.roundabout = None
        self.rot_buffer = None
        self.rot_rate = None
        # self.rate_arr = list()
        # self.rot_arr = list()
        self.angle = list()
        self.old = list()
        self.new = list()
        self.radius = list()
        self.sim_time = 0

        self.point_cloud = []
        self.cloud_state = 0

        self.cpc = None

        self.node = DVnode(cid=211)
        self.node.connect()

        self.connect()
        self.listofmeasurements = dict()
        self.listofenemys = dict()
        self.listofenemys["mycar"] = list()
        self.iteration = 0

        # initHandles
        # self.radar = vrep.simxGetObjectHandle(self.clientID, 'radar', vrepConst.simx_opmode_blocking)[1]
        # vrep.simxGet
        self.car_handle = vrep.simxGetObjectHandle(self.clientID, 'anchor', vrepConst.simx_opmode_blocking)[1]
        self.roundabout = Roundabout(self.clientID, 'Roundabout_center',
                                     [Lane(0.7, 1.5, 'c', VrepObject(self.clientID, 'SphereC')), Lane(1.9, 2.085, 'b', VrepObject(self.clientID, 'SphereB')),
                                      Lane(2.085, 2.285, 'p', VrepObject(self.clientID, 'SphereP'))])
        self.car = VrepObject(self.clientID, 'mycar')

        self.enemys = list()
        self.sim_enemys = list()
        self.sim_enemys.append(Enemy(self.clientID, 'enemy_car1', 'c', 0.93, self))
        self.sim_enemys.append(Enemy(self.clientID, 'enemy_car2', 'c', 0.83, self))
        self.sim_enemys.append(Enemy(self.clientID, 'enemy_car3', 'c', 0.88, self))
        self.sim_enemys.append(Enemy(self.clientID, 'bike', 'b', 0.24, self))
        self.sim_enemys.append(Enemy(self.clientID, 'bike0', 'b', 0.24, self))
        self.sim_enemys.append(Enemy(self.clientID, 'bike1', 'b', 0.24, self))
        self.sim_enemys.append(Enemy(self.clientID, 'Bill_base', 'p', 0.056, self))

    def connect(self):
        print ('Trying to connect..')
        while self.clientID == -1:
            print ("probing..")
            vrep.simxFinish(-1)  # just in case, close all opened connections
            self.clientID = vrep.simxStart('127.0.0.1', self.port, True, True, 5000, vrepConst.simx_opmode_oneshot)
            time.sleep(1)
        print ('Successfully connected to remote API server')

    def norm(self, x):
        return math.sqrt(x[0] ** 2 + x[1] ** 2)

    def update(self):

        print "----------- Time: " + str(self.minutes) + ":" + str(self.seconds) + ":" + str(self.milliseconds)

        self.milliseconds += 50
        self.seconds += self.milliseconds / 1000
        self.milliseconds %= 1000

        self.minutes += self.seconds / 60
        self.seconds %= 60

        for enemy in self.sim_enemys:
            enemy.update(-1)
        self.roundabout.update(self.car_handle)
        self.car.update(-1)

        # estimate rotation Rate (z- axis)
        rot = self.getOrientation()
        if self.rot_buffer == None or rot == None:
            self.rot_buffer = rot
        else:
            if self.rot_buffer - rot > math.pi:
                self.rot_buffer -= 2 * math.pi
            else:
                if self.rot_buffer - rot < -math.pi:
                    self.rot_buffer += 2 * math.pi

            self.rot_rate = (self.rot_buffer - rot) / self.dt
            self.rot_buffer = rot

            # estimate current radius
            alpha = self.rot_rate * self.dt
            if alpha % math.pi != 0:
                b = self.speed * self.dt
                l = 2 * b / alpha * math.sin(alpha / 2)

                r = l / (2 * math.sin(alpha / 2))
                self.radius.append(r)

        Grp1Data_msg = self.node.proto_dict[533]()
        pos = self.car.getPosition() * 10
        wgs84_pos = self.trans.transformToWGS84XY(pos[1], -pos[0])
        Grp1Data_msg.lat = pos[1]  ##wgs84_pos.getLatitude()
        Grp1Data_msg.lon = -pos[0]  # wgs84_pos.getLongitude()
        Grp1Data_msg.roll = 1234

        theta = self.getOrientation()
        if theta is not None:

            # print "Theta: ", theta
            theta = -theta / math.pi * 180

            Grp1Data_msg.heading = float(theta)
        else:
            Grp1Data_msg.heading = 0

        containerGrp1 = self.node.proto_dict[0]()
        containerGrp1.dataType = 533
        containerGrp1.serializedData = Grp1Data_msg.SerializeToString()

        self.node.publish(containerGrp1)

        self.point_cloud += vrep.simxCallScriptFunction(self.clientID, 'velodyneVPL_16', vrep.sim_scripttype_childscript, 'getvel', [], [], [], bytearray(),
                                                        vrepConst.simx_opmode_blocking)[2]
        self.cloud_state += 1
        if self.cloud_state == 2:

            ## cloud is complete:
            angle = np.round(np.array(self.point_cloud[0::3]) / math.pi * 180, 3)
            layer_angle = (np.array(self.point_cloud[1::3]) / math.pi * 180 - 90).round().astype(np.int32)
            ranges = (np.array(self.point_cloud[2::3]) * 1000 + 0.5).astype(np.uint16)

            self.cpc = np.zeros((1803, 16), dtype=np.uint16)

            old_angle = None
            sample_index = 0
            for index, value in enumerate(angle):
                # if ((layer_angle[index] + 15) < 16):
                mapped_angle = int(value * 5 + 0.5) / 5.0
                if mapped_angle != old_angle:
                    sample_index += 1
                # print layer_angle[index]
                self.cpc[int(mapped_angle * 5)][(layer_angle[index] + 15) / 2] = ranges[index]
                old_angle = mapped_angle
            # print sample_index

            shaped_cpc = self.cpc.reshape(1803 * 16)
            msg = self.node.proto_dict[49]()
            msg.distances = shaped_cpc.tobytes()
            msg.startAzimuth = 0
            msg.endAzimuth = 360
            # msg.startAzimuth = 215
            # msg.endAzimuth = -145
            msg.entriesPerAzimuth = 16

            container = self.node.proto_dict[0]()
            container.dataType = 49
            container.serializedData = msg.SerializeToString()
            # container.sent = self.node.proto_dict[12]()
            seconds = int(self.sim_time / 1000)
            microseconds = int(self.sim_time * 1000 - seconds * 1000000)

            # print "seconds: " + str(seconds) + "  :  microseconds: " + str(microseconds)
            container.sent.microseconds = microseconds
            container.sent.seconds = seconds

            self.node.publish(container)
            data = None
            while data == None:
                data = self.conn.recv(4096)
            if data:
                startIndex = data.find("startHere::") + 11
                objects = data[startIndex:].split("::-::")
                msg = self.node.proto_dict[820]()
                newEenemys = []
                for obst in objects[:-1]:
                    msg.ParseFromString(obst)
                    enemy = self.isInEnemys(msg)
                    if (enemy is not None):
                        enemy.update(msg)
                        newEenemys.append(enemy)
                    else:
                        newEenemys.append(DetectionEnemy.DetEnemy(msg, self))
                self.enemys = newEenemys

            for enemy in self.sim_enemys:
                self.listofenemys[enemy.name].append([self.iteration, enemy.getPosition(), enemy.speed, enemy.getOriantation(), enemy.type])
                self.listofenemys["mycar"].append([self.iteration, self.car.getPosition(), self.speed, self.car.getOriantation(), 'self'])
                print [self.iteration, enemy.getPosition(), enemy.speed, enemy.getOriantation(), enemy.type]

            self.iteration += 1

            # print "Bounds:"
            # print angle.min()
            # print angle.max()
            # struct.pack('q', int_)

            self.cloud_state = 0
            self.point_cloud = []

    def getEnemysInRange(self, range):
        enemyInRange = list()
        for enemy in self.enemys:
            if enemy.getDistance() < range:
                enemyInRange.append(enemy)
        return enemyInRange

    def isInEnemys(self, msg):
        for enemy in self.enemys:
            if enemy.id == msg.objId:
                return enemy
        return None

    def getEnemysInRect(self, width, height):
        enemyInRect = list()
        for enemy in self.enemys:
            pos = enemy.getPosition()
            if pos[0] < height and abs(pos[1]) < width / 2:
                enemyInRect.append(enemy)
        return enemyInRect

    def getOrientation(self):
        ret = None
        if self.first:
            ret = vrep.simxGetObjectOrientation(self.clientID, self.car_handle, -1, vrepConst.simx_opmode_streaming)
            self.first = False
        else:
            ret = vrep.simxGetObjectOrientation(self.clientID, self.car_handle, -1, vrepConst.simx_opmode_buffer)
        if ret[0] is 0:
            return ret[1][2]
        return None

    def getBrakingDistance(self):
        t = self.speed / self.neg_accel
        s = (self.speed / 2) * t
        return s
        # return ((self.speed * 3.6) / 10.0) ** 2

    def readProximitySensor(self, handle):
        if handle in self.handleBuffer:
            rem, res, dist, dP, detectedObjectHandle = vrep.simxReadProximitySensor(self.clientID, handle, vrepConst.simx_opmode_buffer)
        else:
            rem, res, dist, dP, detectedObjectHandle = vrep.simxReadProximitySensor(self.clientID, handle, vrepConst.simx_opmode_streaming)
            self.handleBuffer.append(handle)
        if res > 0:
            return np.linalg.norm(dist)
        else:
            return self.max_dist

    def run(self):
        vrep.simxStopSimulation(self.clientID, vrep.simx_opmode_blocking)
        print "Stopped"
        time.sleep(5)
        vrep.simxSynchronous(self.clientID, True)
        vrep.simxStartSimulation(self.clientID, vrep.simx_opmode_blocking)

        while True:
            self.update()
            ##self.gobals.dt = 0.9 * self.gobals.dt + 0.1 * (time.time() - self.gobals.time)
            self.time = time.time()
            self.currentState.run()

            dv = self.accel * self.dt
            if self.speed + dv <= self.target_speed:
                self.speed += dv

            if self.speed > self.target_speed:
                dv = self.neg_accel * self.dt
                self.speed -= dv
            self.speed = max((0, self.speed))

            vrep.simxWriteStringStream(self.clientID, "speed", vrep.simxPackFloats([self.speed]), vrep.simx_opmode_oneshot)
            vrep.simxSynchronousTrigger(self.clientID)
            self.sim_time += 50
            time.sleep(0.0)

    def setSpeed(self):
        dv = self.accel * self.dt
        if self.speed + dv <= self.target_speed:
            self.speed += dv

        if self.speed > self.target_speed:
            dv = self.neg_accel * self.dt
            self.speed -= dv
        self.speed = max((0, self.speed))


tmp = CarLogic(port=19997)

try:
    tmp.run()

except KeyboardInterrupt:
    tmp.conn.close()
    vrep.simxPauseSimulation(tmp.clientID, vrep.simx_opmode_blocking)
    vrep.simxFinish(-1)

finally:
    print "Close Connection"
    tmp.conn.close()
    vrep.simxFinish(tmp.clientID)
    # self.listofmeasurements = dict()
    ## self.listofenemys = dict()
    #pickle.dump(tmp.listofmeasurements, open("measurements.p", "wb"))
    #pickle.dump(tmp.listofenemys, open("simulation.p", "wb"))

# plt.plot(tmp.speed_array)
# plt.plot(tmp.alpha_array)
# plt.plot(tmp.angle,'b')
# plt.plot(tmp.new,'g')
# plt.plot(tmp.old,'r')
# plt.plot(tmp.rate_arr)
# plt.plot(tmp.radius)
# plt.plot(tmp.angle)
# plt.show()
