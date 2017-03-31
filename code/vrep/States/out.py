import States


class DriveOutRoundabout:
    def __init__(self, globals):
        self.globals = globals
        self.name = "DriveOutRoundabout"
        self.intialSpeed = self.globals.speed
        self.brake = None

    def setBrakeDistance(self, distance):
        if self.brake == None:
            self.brake = distance
        elif distance < self.brake:
            self.brake = distance

    def run(self):
        mypos = self.globals.car.getPosition() * 10
        line_segments = self.globals.parser.scenario.getLineSegments(mypos)
        if len(line_segments) > 0:
            print "Roadname: ", line_segments[-1][0].parent.parent.name
        else:
            print "Roadname: None"
        print ""
        print "-----------------------------------------"
        print "State: \033[1;33m" + str(self.name) + "\033[0m"
        print "-----------------------------------------"
        print "Roundabout distance: ", self.globals.roundabout.getDistance()
        print "MyCar Speed: ", self.globals.speed

        self.globals.target_speed = self.globals.max_speed
        self.brake = None

        if len(line_segments) > 0:
            if line_segments[-1][0].parent.parent.name == "South":
                self.globals.currentState = States.ToRoundabout(self.globals)

        enemys = self.globals.getEnemysInRange(1)

        for enemy in enemys:
            enemy.mapToLane()
            enemy.printStats()

            pos = enemy.getPosition()
            if pos[0] > -0.3 and pos[1] > 0:
                if enemy.lane is not None:
                    distance = enemy.lane.inner_r - self.globals.roundabout.getDistance() - self.globals.car_length / 2 - 0.05
                    self.setBrakeDistance(distance)

        if self.brake is not None:
            print "\033[1;33m------------------------------State_Change----------------------------------\033[0m"
            self.globals.currentState = States.Brake(self.globals, self.brake, DriveOutRoundabout(self.globals))
            self.globals.currentState.run()
