#!/usr/bin/env python

import math
import time

import matplotlib.pyplot as plt
import numpy as np

from VrepObject import VrepObject
from lane import Lane
from remoteApi import vrep
from remoteApi import vrepConst


class Autonomous:
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
        self.car_length = 0.5
        self.max_neg_accel = 1.1

        self.roundabout_radius = 0.75
        self.handleBuffer = []
        self.state = 0

        self.roundabout_lanes = [Lane(0.5, 1.0, 'c'), Lane(1.1, 1.3, 'b'), Lane(1.3, 1.55, 'p')]

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

        self.enemys = list()
        self.enemys.append(VrepObject(self.clientID, 'enemy_car1'))
        self.enemys.append(VrepObject(self.clientID, 'enemy_car2'))
        # self.enemys.append(VrepObject(self.clientID, 'enemy_bicycle1'))
        # self.enemys.append(VrepObject(self.clientID, 'Bill_base'))
        self.roudabout = VrepObject(self.clientID, 'Roundabout_center')

    def update(self):
        for enemy in self.enemys:
            enemy.update(self.car_handle)
        self.roudabout.update(self.car_handle)

    def getEnemysInRange(self, range):
        enemyInRange = list()
        for enemy in self.enemys:
            if enemy.getDistance() < range:
                enemyInRange.append(enemy)
        return enemyInRange

    def getBrakingDistance(self):
        return ((self.speed * 3.6) / 10.0) ** 2

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

    def getObjSpeed(self):
        pass

    def run(self):

        vrep.simxStopSimulation(self.clientID, vrep.simx_opmode_blocking)
        vrep.simxSynchronous(self.clientID, True)
        time.sleep(1)
        vrep.simxStartSimulation(self.clientID, vrep.simx_opmode_blocking)

        res, objs = vrep.simxGetObjects(self.clientID, vrep.sim_handle_all, vrep.simx_opmode_blocking)
        print objs
        blocked = dict()

        while True:
            self.update()
            ##self.dt = 0.9 * self.dt + 0.1 * (time.time() - self.time)
            self.time = time.time()
            self.target_speed = self.max_speed

            print ""
            print "-----------------------------------------"
            print "Roundabout distance: ", self.roudabout.getDistance()
            if self.state == 0 and self.roudabout.getDistance() < 1:
                self.state = 1
            if self.state == 1 and self.roudabout.getDistance() > 3:
                self.state = 0

            if self.state == 0:
                # print "Roundabout pos: ", self.roudabout.getPosition()
                enemys = self.getEnemysInRange(3)
                for enemy in enemys:
                    # New
                    # reset dynamic paramters
                    enemy.lane = None

                    # ---------------------- assign enemy to lane --------------------
                    r_dist = self.norm(enemy.getPosition() - self.roudabout.getPosition())
                    for lane in self.roundabout_lanes:  #
                        # calculate enemy roundabout distance
                        if r_dist < lane.outer_r and r_dist > lane.inner_r:
                            enemy.lane = lane

                    print "Enemy Type: ", enemy.lane.type

                    # ---------------- estimate enemy speed on lane ------------------
                    if enemy.lane is not None:
                        # calculate intersection position
                        intersection_position = self.roudabout.getPosition()
                        intersection_position[0] -= enemy.lane.r
                        # calculate object -- intersection distance
                        a = self.norm(intersection_position - enemy.getPosition())

                        # get roundabout angle with Law of cosines
                        b = c = enemy.lane.r
                        # print "a: ", a
                        # print "b: ", b
                        # print "c: ", c

                        if (b ** 2 + c ** 2 - a ** 2) < 0:
                            # roundabout distorted or data noisy
                            # raise AttributeError('roundabout distorted or data to noisy')
                            enemy.speed = None
                            enemy.intersection_distance = None
                            # print "-------------------------------reset--------------------------------------"
                        else:
                            alpha = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c))
                            # print "alpha ", alpha / math.pi * 180
                            # calculate enemy intersection distance
                            enemy_intersection_distance = (alpha / (2 * math.pi)) * (math.pi * 2 * enemy.lane.r)

                            print "Enemy " + str(enemy.name) + "." + str(enemy.lane.type) + " Intersection Distance: ", enemy_intersection_distance

                            # estimate speed with given movement change
                            if enemy.intersection_distance is None:
                                enemy.intersection_distance = enemy_intersection_distance
                            else:
                                estimated_speed = (enemy.intersection_distance - enemy_intersection_distance) / self.dt
                                enemy.intersection_distance = enemy_intersection_distance
                                if enemy.speed is not None:
                                    enemy.speed = 0.8 * enemy.speed + 0.2 * estimated_speed
                                else:
                                    enemy.speed = estimated_speed
                                # enemy.speed = estimated_speed

                                print "Enemy " + str(enemy.name) + "." + str(enemy.lane.type) + " Speed:", estimated_speed

                    if enemy.speed is not None and enemy.intersection_distance is not None:
                        if enemy.lane.type != 'c':

                            enemy_timewindow = abs(enemy.intersection_distance / enemy.speed)

                            deltav = self.max_speed - self.speed
                            t = deltav / self.accel
                            s = 0
                            if enemy_timewindow - t < 0:
                                s = (self.accel / 2) * enemy_timewindow * enemy_timewindow + self.speed * enemy_timewindow

                            else:
                                s = ((self.accel / 2) * t * t + self.speed * t) + (enemy_timewindow - t) * self.max_speed

                            goal_distance = self.roudabout.getDistance() - enemy.lane.inner_r + self.car_length / 2
                            stop_distance = self.roudabout.getDistance() - 1.55 - self.car_length / 2
                            print "Goal: ", goal_distance
                            print "Stop: ", stop_distance
                            print "Car: ", s
                            if s < goal_distance and s > stop_distance:
                                print "Stop Not Car"
                                print "time: ", enemy_timewindow
                                print "Speed: ", self.speed
                                self.target_speed = 0
                                # self.neg_accel = abs(self.speed / enemy_timewindow)
                                # print "resulting accel: ", self.neg_accel
                                # if self.neg_accel > self.max_neg_accel:
                                #    vrep.simxPauseSimulation(tmp.clientID, vrep.simx_opmode_blocking)
                                #    print "--------------------------ERROR________________________________"
                                #    raise AttributeError('acceleration to large', self.neg_accel)

                        if enemy.lane.type == 'c':
                            if enemy.speed >= 0:

                                enemy_timewindow = abs(enemy.intersection_distance / enemy.speed)

                                deltav = self.max_speed - self.speed
                                t = deltav / self.accel
                                s = 0
                                if enemy_timewindow - t < 0:
                                    s = (self.accel / 2) * enemy_timewindow * enemy_timewindow + self.speed * enemy_timewindow

                                else:
                                    s = ((self.accel / 2) * t * t + self.speed * t) + (enemy_timewindow - t) * self.max_speed

                                goal_distance = self.roudabout.getDistance() - enemy.lane.r + self.car_length
                                stop_distance = self.roudabout.getDistance() - enemy.lane.outer_r - self.car_length
                                print "Goal: ", goal_distance
                                print "Stop: ", stop_distance
                                print "Car: ", s
                                if s < goal_distance and s > stop_distance:
                                    print "Stop Car"
                                    print "time: ", enemy_timewindow
                                    print "Speed: ", self.speed
                                    self.target_speed = 0

                            else:
                                enemy_timewindow = abs((self.car_length - enemy.intersection_distance) / enemy.speed)
                                deltav = self.max_speed - self.speed
                                t = deltav / self.accel
                                s = 0
                                if enemy_timewindow - t < 0:
                                    s = (self.accel / 2) * enemy_timewindow * enemy_timewindow + self.speed * enemy_timewindow

                                else:
                                    s = ((self.accel / 2) * t * t + self.speed * t) + (enemy_timewindow - t) * self.max_speed

                                stop_distance = self.roudabout.getDistance() - enemy.lane.outer_r - self.car_length/2
                                print "Stop Distance: ", stop_distance
                                print "MyCar Distance: ", s
                                print "Enemy Timewindow: ", enemy_timewindow
                                print "speed: ", enemy.speed
                                print "enemy.intersection_distance: ", enemy.intersection_distance
                                brake_dist = self.getBrakingDistance()

                                if enemy.intersection_distance < self.car_length and brake_dist > stop_distance - self.car_length:
                                    print "Stopped by car to close.."
                                    #raw_input("Press Enter to continue...")
                                    #raw_input("Press Enter to continue...")
                                    self.target_speed = 0

            dv = self.accel * self.dt
            if self.speed + dv <= self.target_speed:
                self.speed += dv

            if self.speed > self.target_speed:
                dv = self.neg_accel * self.dt
                self.speed -= dv
            self.speed = max((0, self.speed))

            vrep.simxWriteStringStream(self.clientID, "speed", vrep.simxPackFloats([self.speed]), vrep.simx_opmode_oneshot)
            time.sleep(0.044)
            vrep.simxSynchronousTrigger(self.clientID)


tmp = Autonomous(port=19997)
tmp.connect()
tmp.initHandles()

try:
    tmp.run()
except KeyboardInterrupt:
    vrep.simxPauseSimulation(tmp.clientID, vrep.simx_opmode_blocking)
    vrep.simxFinish(-1)
plt.plot(tmp.speed_array)
# plt.show()
