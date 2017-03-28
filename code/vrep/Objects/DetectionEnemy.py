import math

import numpy as np

from VrepObject import VrepObject


class DetEnemy():
    def __init__(self, msg, globals):
        print msg.objId
        self.globals = globals
        self.speed = None
        self.distance_hist = None
        self.lane = None

        self.intersection_distance = None
        self.oldPosition = None
        self.speedVector = None
        self.pos = [msg.pos_y / 10.0, -msg.pos_x / 10.0, 0]

        self.id = msg.objId
        self.name = msg.objId
        self.yawrate = msg.yaw_rate
        self.speed = msg.speed / 10.0
        self.theta = msg.theta
        if msg.type == 1:
            self.type = 'c'
        elif msg.type == 2:
            self.type = 'b'
        elif msg.type == 3:
            self.type = 'p'
        else:
            self.type = msg.type

    def update(self, msg):
        print msg.objId
        self.pos = [msg.pos_y / 10.0, -msg.pos_x / 10.0, 0]
        self.id = msg.objId
        self.yawrate = msg.yaw_rate
        self.speed = msg.speed / 10.0
        self.theta = msg.theta
        if msg.type == 1:
            self.type = 'c'
        elif msg.type == 2:
            self.type = 'b'
        elif msg.type == 3:
            self.type = 'p'
        else:
            self.type = msg.type

    def getPosition(self):
        return self.pos

    def getDistance(self):
        return math.sqrt(self.pos[0] * self.pos[0] + self.pos[1] * self.pos[1])

    def mapToLane(self):
        # ---------------------- assign enemy to lane --------------------
        r_dist = self.globals.norm(self.getPosition()-self.globals.roundabout.getPosition())
        print "Roundabout dist: ", r_dist
        for lane in self.globals.roundabout.lanes:  #
            if r_dist < lane.outer_r and r_dist > lane.inner_r:
                self.lane = lane

    def printStats(self):
        print "----------------\033[1;33m" + str(self.name) + "\033[0m---------------- "
        print "Pos: X: " + str(self.pos[0]) + " Y: " + str(self.pos[1])
        print "Type: ", self.type
        if self.speed is not None:
            print('Speed: % .2f' % self.speed)
        else:
            print "Speed: ", self.speed
        if self.lane is not None:
            print "Lane: ", self.lane.type

        if self.speedVector is not None:
            print "SpeedVector: ", self.speedVector

    def estimateSpeed(self):
        # ---------------- estimate enemy speed on lane ------------------
        # print "----------------" + str(self.name) + "----------------"
        # print "fuck: ",self.lane
        if self.lane is not None:
            # calculate intersection position
            intersection_position = self.globals.roundabout.getPosition()
            alpha = math.atan2(intersection_position[0], -intersection_position[1]) - (math.pi / 2)
            intersection_position[0] -= self.lane.r
            b = self.globals.norm(self.globals.roundabout.getPosition())
            a = self.lane.r
            if -1 <= ((math.sin(alpha) * b) / a) <= 1:
                beta = math.pi - math.asin((math.sin(alpha) * b) / a)  # mehrere loesungen!!!!! SSW Dreieck
                gamma = math.pi - alpha - beta
                d = (a * math.sin(gamma)) / math.sin(alpha)
                if self.type == 'c':
                    # self.globals.angle.append(alpha * 180 / math.pi)  # 360 * alpha / math.pi) #b
                    # self.globals.new.append(beta * 180 / math.pi)  # d)  # 360 * alpha / math.pi) #g
                    # self.globals.old.append(gamma * 180 / math.pi)  # self.globals.norm(intersection_position)) #r
                    self.globals.debug.setPosition([d, 0, 0.2], self.globals.car_handle)

                intersection_position = np.array([d, 0, 0])
            else:
                # print "intersection_position far away.."
                intersection_position = np.array([999, 0, 0])  ## far away

            # calculate object -- intersection distance
            a = self.globals.norm(intersection_position - self.getPosition())

            # get roundabout angle with Law of cosines
            b = c = self.lane.r
            # print "a: ", a
            # print "b: ", b
            # print "c: ", c
            # print "acos :", ((b ** 2 + c ** 2 - a ** 2) / (2 * b * c))
            # print "\033[1;33mArccos: + " + str((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)) + "\033[0m"
            if not (-1 <= ((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)) <= 1):
                # roundabout distorted or data noisy
                # raise AttributeError('roundabout distorted or data to noisy')
                #self.speed = None
                self.intersection_distance = None
                # print "-------------------------------reset--------------------------------------"
            else:
                print "Intersection Calculated!!"
                alpha = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c))
                # calculate enemy intersection distance
                enemy_intersection_distance = (alpha / (2 * math.pi)) * (math.pi * 2 * self.lane.r)

                # print "Enemy " + str(self.name) + "." + str(self.lane.type) + " Intersection Distance: ", enemy_intersection_distance

                # estimate speed with given movement change
                if self.intersection_distance is None:
                    self.intersection_distance = enemy_intersection_distance
                else:
                    estimated_speed = (self.intersection_distance - enemy_intersection_distance) / self.globals.dt
                    if self.type == 'p':
                        self.globals.speed_array.append(estimated_speed)
                        self.globals.alpha_array.append(alpha)
                        self.globals.b.append(enemy_intersection_distance)

                    self.intersection_distance = enemy_intersection_distance
                    sign = lambda a: (a > 0) - (a < 0)
                    # if self.speed is not None:
                    #     self.speed = (0.8 * abs(self.speed) + 0.2 * abs(estimated_speed)) * sign(estimated_speed)
                    # else:
                    #     self.speed = estimated_speed

    def estimateSpeedSimpe(self):
        # ---------------- estimate enemy speed on lane ------------------
        if self.lane is not None:

            # aprximate object -- intersection distance with pythagoras
            b = self.globals.roundabout.getDistance() - self.lane.r
            c = self.getDistance()

            if c ** 2 < b ** 2:
                # roundabout distorted or data noisy
                # raise AttributeError('roundabout distorted or data to noisy')
                self.speed = None
                self.intersection_distance = None
                # print "-------------------------------reset--------------------------------------"
            else:
                intersection_distance = math.sqrt((c ** 2 - b ** 2))

                # print "Enemy " + str(self.name) + "." + str(self.lane.type) + " Intersection Distance: ", enemy_intersection_distance

                # estimate speed with given movement change
                if self.intersection_distance is None:
                    self.intersection_distance = intersection_distance
                else:
                    estimated_speed = (self.intersection_distance - intersection_distance) / self.globals.dt
                    self.intersection_distance = intersection_distance
                    sign = lambda a: (a > 0) - (a < 0)
                    if self.speed is not None:
                        self.speed = (0.8 * abs(self.speed) + 0.2 * abs(estimated_speed)) * sign(estimated_speed)
                    else:
                        self.speed = estimated_speed

    def estimateSpeedNew(self):
        print  "dt: ", self.globals.dt
        if self.oldPosition is None:
            self.oldPosition = self.getPosition()

        else:
            newPos = self.getPosition()

            print "OldPos: ", self.oldPosition
            print "newPos: ", newPos
            estimated_speed = (newPos - self.oldPosition) / self.globals.dt
            print "deltaPos: ", newPos - self.oldPosition
            self.oldPosition = self.getPosition()
            estimated_speed[0] += self.globals.speed

            # if self.speed is not None:
            #    self.speed = 0.8 * self.speed + 0.2 * estimated_speed
            # else:
            self.speed = self.globals.norm(estimated_speed)
            self.speedVector = estimated_speed
