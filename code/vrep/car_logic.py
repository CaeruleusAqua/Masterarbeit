#!/usr/bin/env python

import math
import time

import matplotlib.pyplot as plt
import numpy as np
from objects.Enemy import Enemy
from objects.Roundabout import Roundabout
from objects.lane import Lane

from States.startState import StartState
from objects.VrepObject import VrepObject
from remoteApi import vrep
from remoteApi import vrepConst


class CarLogic:
    def __init__(self, port):
        self.clientID = -1
        self.port = port

        ## Parameters:
        self.time = time.time()
        self.speed = 0.33
        self.target_speed = 0.83
        self.max_speed = 0.83
        self.length = 0
        self.dt = 0.05
        self.accel = 1.0
        self.neg_accel = 1.1
        self.max_dist = 30
        self.speed_array = list()
        self.alpha_array = list()
        self.b = list()
        self.car_length = 0.5
        self.max_neg_accel = 1.1
        self.first = True

        self.handleBuffer = []

        self.currentState = StartState(self)
        self.roundabout = None
        self.rot_buffer = None
        self.rot_rate = None
        #self.rate_arr = list()
        #self.rot_arr = list()
        self.angle = list()
        self.old = list()
        self.new = list()
        self.radius = list()

    def connect(self):
        print ('Trying to connect..')
        while self.clientID == -1:
            print ("probing..")
            vrep.simxFinish(-1)  # just in case, close all opened connections
            self.clientID = vrep.simxStart('127.0.0.1', self.port, True, True, 5000, vrepConst.simx_opmode_oneshot)
            time.sleep(1)
        print ('Successfully connected to remote API server')

    def norm(self, x):
        return math.sqrt(x[0] ** 2 + x[1] ** 2 + x[2] ** 2)

    def initHandles(self):
        self.radar = vrep.simxGetObjectHandle(self.clientID, 'radar', vrepConst.simx_opmode_blocking)[1]
        self.car_handle = vrep.simxGetObjectHandle(self.clientID, 'anchor', vrepConst.simx_opmode_blocking)[1]
        self.roundabout = Roundabout(self.clientID, 'Roundabout_center',[Lane(0.5, 1.0, 'c'), Lane(1.1, 1.3, 'b'), Lane(1.3, 1.55, 'p')])
        self.debug = VrepObject(self.clientID, 'Sphere')
        # self.intersection = VrepObject(self.clientID, 'intersect')

        self.enemys = list()
        self.enemys.append(Enemy(self.clientID, 'enemy_car1', 'c', self))
        self.enemys.append(Enemy(self.clientID, 'enemy_car2', 'c', self))
        self.enemys.append(Enemy(self.clientID, 'enemy_bicycle1', 'b', self))
        self.enemys.append(Enemy(self.clientID, 'Bill_base', 'p', self))

    def update(self):
        for enemy in self.enemys:
            enemy.update(self.car_handle)
        self.roundabout.update(self.car_handle)
        # self.intersection.update(self.car_handle)


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
            #print "Rotrate: ", self.rot_rate
            #self.rot_arr.append(rot)
            #self.rate_arr.append(self.rot_rate)

            # estimate current radius
            alpha = self.rot_rate*self.dt
            if alpha % math.pi != 0:
                b = self.speed*self.dt
                l = 2*b/alpha * math.sin(alpha/2)

                r = l/(2*math.sin(alpha/2))
                self.radius.append(r)


    def getEnemysInRange(self, range):
        enemyInRange = list()
        for enemy in self.enemys:
            if enemy.getDistance() < range:
                enemyInRange.append(enemy)
        return enemyInRange

    def getEnemysInRect(self,width,height):
        enemyInRect = list()
        for enemy in self.enemys:
            pos = enemy.getPosition()
            if pos[0]< height and abs(pos[1])< width/2 :
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
        vrep.simxSynchronous(self.clientID, True)
        time.sleep(1)
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
            time.sleep(0.145)

    def setSpeed(self):
        dv = self.accel * self.dt
        if self.speed + dv <= self.target_speed:
            self.speed += dv

        if self.speed > self.target_speed:
            dv = self.neg_accel * self.dt
            self.speed -= dv
        self.speed = max((0, self.speed))


tmp = CarLogic(port=19997)
tmp.connect()
tmp.initHandles()

try:
    tmp.run()
except KeyboardInterrupt:
    vrep.simxPauseSimulation(tmp.clientID, vrep.simx_opmode_blocking)
    vrep.simxFinish(-1)

# plt.plot(tmp.speed_array)
# plt.plot(tmp.alpha_array)
#plt.plot(tmp.angle,'b')
#plt.plot(tmp.new,'g')
#plt.plot(tmp.old,'r')
# plt.plot(tmp.rate_arr)
#plt.plot(tmp.radius)
#plt.show()
