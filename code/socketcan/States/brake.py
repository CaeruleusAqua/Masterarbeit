class Brake:
    def __init__(self, globals, distance, nextState):
        self.globals = globals
        self.name = "BrakingState"
        self.nextState = nextState
        self.distance = distance
        self.intialSpeed = self.globals.speed

    def run(self):
        print ""
        print "-----------------------------------------"
        print "State: \033[1;33m" + str(self.name) + "\033[0m"
        print "-----------------------------------------"
        print "Roundabout distance: ", self.globals.roundabout.getDistance()
        print "MyCar Speed: ", self.globals.speed
        print "Branking in: ", self.distance

        if self.globals.speed == 0:
            print "\033[1;33m------------------------------State_Change----------------------------------\033[0m"
            # print "------------------------------Waiting 1Sek----------------------------------"
            # time.sleep(1)
            self.globals.currentState = self.nextState
            return

        # calculating acceleration
        t = self.distance / (self.intialSpeed / 2)
        if t != 0:
            neg_accel = min((self.intialSpeed / t, self.globals.max_neg_accel))
            if neg_accel < 0:
                neg_accel = self.globals.max_neg_accel
        else:
            neg_accel = self.globals.max_neg_accel

        neg_accel = max((neg_accel, 0.001))
        self.globals.neg_accel = neg_accel
        self.globals.target_speed = 0

        print "Acceleration: ", -self.globals.neg_accel
