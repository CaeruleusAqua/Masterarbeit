from States.toRoundabout import ToRoundaboutState


class StartState:
    def __init__(self, globals):
        self.globals = globals
        self.name = "startStat"

    def run(self):
        self.globals.target_speed = self.globals.max_speed

        print ""
        print "-----------------------------------------"
        print "State: \033[1;33m" + str(self.name) + "\033[0m"
        print "-----------------------------------------"
        print "Roundabout distance: ", self.globals.roundabout.getDistance()
        if self.globals.roundabout.getDistance() < 3:
            print "\033[1;33m------------------------------State_Change----------------------------------\033[0m"
            self.globals.currentState = ToRoundaboutState(self.globals)

        self.globals.setSpeed()
