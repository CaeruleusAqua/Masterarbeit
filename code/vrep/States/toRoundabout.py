import States
import math
import numpy as np


class ToRoundabout:
    def __init__(self, globals):
        self.globals = globals
        self.name = "ToRoundaboutState"
        self.brake = None

    def setBrakeDistance(self, distance):
        if self.brake == None:
            self.brake = distance
        elif distance < self.brake:
            self.brake = distance

    def run(self):

        print ""
        print "-----------------------------------------"
        print "State: \033[1;33m" + str(self.name) + "\033[0m"
        print "-----------------------------------------"
        print "Roundabout distance: ", self.globals.roundabout.getDistance()
        print "Branking Distance: ", self.globals.getBrakingDistance()
        print "MyCar Speed: ", self.globals.speed
        mypos = self.globals.car.getPosition() * 10
        #line_segments = self.globals.parser.scenario.getLineSegments(mypos)
        #print "Roadname: ", line_segments[-1][0].parent.parent.name
        # for seg in line_segments:
        #     print "Roadname: ",seg[0].parent.parent.name



        # calculate intersection positions
        for lane in self.globals.roundabout.lanes:
            intersection_position = self.globals.roundabout.getPosition()
            alpha = math.atan2(intersection_position[0], -intersection_position[1]) - (math.pi / 2)
            intersection_position[0] -= lane.r
            b = self.globals.norm(self.globals.roundabout.getPosition())
            a = lane.r
            if -1 <= ((math.sin(alpha) * b) / a) <= 1:
                beta = math.pi - math.asin((math.sin(alpha) * b) / a)  # mehrere loesungen!!!!! SSW Dreieck
                gamma = math.pi - alpha - beta
                d = (a * math.sin(gamma)) / math.sin(alpha)

                lane.debug.setPosition([d, 0, 0.02], self.globals.car_handle)

                intersection_position = np.array([d, 0, 0])
            else:
                # print "intersection_position far away.."
                intersection_position = None
            lane.intersection_position = intersection_position
            # line_segments = self.globals.parser.scenario.getLineSegments(intersection_position * 10)
            # for segment in line_segments:
            #     lane.lineSegment = segment[0]
            #     lane.posInLineSegment = segment[1]

        self.globals.target_speed = self.globals.max_speed
        self.brake = None

        # enemys = self.globals.getEnemysInRange(3)
        enemys = self.globals.enemys

        if self.globals.roundabout.getDistance() - 1 < self.globals.car_length / 2:
            print "\033[1;33m------------------------------State_Change----------------------------------\033[0m"
            self.globals.currentState = States.AdaptiveCruiseControl(self.globals)
            return

        for enemy in enemys:

            # reset dynamic paramters
            # enemy.lane = None

            # ---------------------- assign enemy to lane and estimatespeed --------------------
            enemy.mapToLane()
            # if enemy.lane is not None:
            #     enemy.estimateSpeed()

            # enemy.mapToLineSegment()

            enemy.printStats()
            # print "lineSegment: ", enemy.lineSegment
            # print "lane: ", enemy.lane
            # if enemy.lineSegment is not None:
            #     print "Road: ",enemy.lineSegment[0].parent.parent.name
            #     print "LaneID: ",enemy.lineSegment[0].parent.id
            #
            #
            # if enemy.lineSegment is not None and enemy.lane is not None and enemy.lane.lineSegment is not None and enemy.lineSegment[0] is not None:
            #     if enemy.lane.lineSegment.parent == enemy.lineSegment[0].parent:
            #         print "lineSegment: ", enemy.lineSegment[0]
            #         print "lane: ", enemy.lane.lineSegment
            #         print "enemy_distance: ", self.globals.parser.scenario.getDistance(enemy.lineSegment[0],enemy.lane.lineSegment)
            #     else:
            #         print "comparing unequal lanes!--------------------------------------------------------------------------------------------"



            intersection_distance = enemy.getIntersectionDistance()
            print "intersection_distance: ", intersection_distance

            lane_dist = self.globals.roundabout.getDistance() - self.globals.roundabout.outer_r
            brake_dist = self.globals.getBrakingDistance() + self.globals.car_length + 0.2
            if lane_dist <= brake_dist and enemy.speed is not None and intersection_distance is not None:
                if intersection_distance > 0:

                    enemy_timewindow = abs(intersection_distance / enemy.speed)

                    deltav = self.globals.max_speed - self.globals.speed
                    t = deltav / self.globals.accel
                    s = 0
                    if enemy_timewindow - t < 0:
                        s = (self.globals.accel / 2) * enemy_timewindow * enemy_timewindow + self.globals.speed * enemy_timewindow

                    else:
                        s = ((self.globals.accel / 2) * t * t + self.globals.speed * t) + (enemy_timewindow - t) * self.globals.max_speed

                    goal_distance = self.globals.roundabout.getDistance() - enemy.lane.r + self.globals.car_length
                    stop_distance = self.globals.roundabout.getDistance() - 1.55 - self.globals.car_length
                    print "Goal distance: ", goal_distance
                    print "Stop distance: ", stop_distance
                    print "Estimated Car distance: ", s
                    print "Estimated Time Window: ", enemy_timewindow

                    if s < goal_distance and s > stop_distance:
                        print "Stop Caused my: ", enemy.name
                        self.setBrakeDistance(self.globals.roundabout.getDistance() - 1.55 - self.globals.car_length / 2)

        if self.brake is not None:
            print "\033[1;33m------------------------------State_Change----------------------------------\033[0m"
            self.globals.currentState = States.Brake(self.globals, self.brake, ToRoundabout(self.globals))
            self.globals.currentState.run()
