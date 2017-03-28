import States


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

        self.globals.target_speed = self.globals.max_speed
        self.brake = None

        #enemys = self.globals.getEnemysInRange(3)
        enemys = self.globals.enemys

        if self.globals.roundabout.getDistance() - 1 < self.globals.car_length / 2:
            print "\033[1;33m------------------------------State_Change----------------------------------\033[0m"
            self.globals.currentState = States.AdaptiveCruiseControl(self.globals)
            return

        for enemy in enemys:

            # reset dynamic paramters
            enemy.lane = None

            # ---------------------- assign enemy to lane and estimatespeed --------------------
            enemy.mapToLane()
            if enemy.lane is not None:
                enemy.estimateSpeed()

            enemy.printStats()

            lane_dist = self.globals.roundabout.getDistance() - self.globals.roundabout.outer_r
            brake_dist = self.globals.getBrakingDistance() + self.globals.car_length + 0.2
            if lane_dist <= brake_dist and enemy.speed is not None and enemy.intersection_distance is not None:
                if enemy.speed > 0:

                    enemy_timewindow = abs(enemy.intersection_distance / enemy.speed)

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

                if enemy.speed < 0:
                    # range_to_target_lane =
                    enemys = self.globals.getEnemysInRect(0.5, 1)
                    print "\033[1;33mEnemys in Rect: + " + str(enemys) + "\033[0m"
                    if len(enemys) != 0:
                        self.setBrakeDistance(self.globals.roundabout.getDistance() - 1.55 - self.globals.car_length / 2)

        if self.brake is not None:
            print "\033[1;33m------------------------------State_Change----------------------------------\033[0m"
            self.globals.currentState = States.Brake(self.globals, self.brake, ToRoundabout(self.globals))
            self.globals.currentState.run()
