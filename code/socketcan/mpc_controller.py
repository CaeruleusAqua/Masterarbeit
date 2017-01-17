#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import threading

import opendavinci.odvdvehicle_pb2 as odvdVehicle
import opendavinci.odvdxc90_pb2 as odvdXC90
import opendavinci.opendavinci_pb2 as odvd
from mpc_model import OdeModel
from opendavinci.DVnode import DVnode
from tools import Rate
from tools import getch
import math

max_accel = 2
min_accel = -1


class Controller:
    def __init__(self, p_gain):
        self.model = OdeModel()
        self.acceleration = 0
        self.steering = 0
        self.enable = False
        self.pgain = p_gain
        self.igain = 0
        self.dgain = 0
        self.dt = 1 / 50.0
        self.esum = 0
        self.ealt = 0
        self.velocity = 0.0
        self.radstand = 4

    def incAccel(self, value):
        accel = self.acceleration + value;
        self.acceleration = round(min(max(accel, min_accel), max_accel), 4)

    def getSteeringRequest(self, point):
        e = point.y
        self.esum = self.esum + e
        y = self.pgain * e + self.igain * self.dt * self.esum + self.dgain * (e - self.ealt) / self.dt
        self.ealt = e
        return y

    def getVelSteeringRequest(self, point):
        c = float(math.sqrt(point.x**2 + point.y**2))
        alpha = math.asin(point.y/c)
        delta = math.atan((self.pgain*alpha*self.radstand)/c)
        return delta
    0

def targetPointCallback(msg, timeStamps):
    global controll, lock
    if controll.enable:
        lock.acquire()
        controll.steering = controll.getSteeringRequest(msg)
        lock.release()


def carSpeedCallback(msg, timeStamps):
    global controll, lock
    lock.acquire()
    controll.velocity = msg.VehicleLgtSpeed
    lock.release()


assert len(sys.argv) == 2
pgain = float(sys.argv[1])
print "P-Gain: ", pgain

controll = Controller(pgain)
node = DVnode(cid=214)
node.registerCallback(999, targetPointCallback, odvdVehicle.opendlv_legacy_TargetPoint)
node.registerCallback(512, carSpeedCallback, odvdXC90.opendlv_proxy_reverexc90_CarSpeed)
node.connect()
rate = Rate(100)
lock = threading.Lock()

finished = False


def Input_Thread():
    global finished, controll, lock
    try:
        while not finished:
            input = getch()
            print ">" + input
            # print("Deine Eingabe-> %s" % ord(input))
            if input == "q" or ord(input) == 3:
                print("quit")
                finished = True
            lock.acquire()
            if ord(input) == 13:
                controll.acceleration = 0
                print "Rest to Zero"
            if input == 'w':
                controll.incAccel(0.05)
                print "Accel: ", controll.acceleration
            if input == 's':
                controll.incAccel(-0.05)
                print "Accel: ", controll.acceleration
            if input == 'a':
                controll.steering += 0.5
                print "Steering: ", controll.steering
            if input == 'd':
                controll.steering -= 0.5
                print "Steering: ", controll.steering
            if input == 'c':
                controll.enable = not controll.enable
                print "Controlled: ", controll.enable
            lock.release()

    except (KeyboardInterrupt, SystemExit):
        finished = True


thread2 = threading.Thread(target=Input_Thread)
thread2.start()

while not finished:
    message = odvdVehicle.opendlv_proxy_ActuationRequest()
    lock.acquire()
    message.acceleration = controll.acceleration
    message.steering = controll.steering
    lock.release()
    message.isValid = 1
    container = odvd.odcore_data_MessageContainer()
    container.serializedData = message.SerializeToString()
    container.dataType = 160
    node.publish(container)
    rate.sleep()
