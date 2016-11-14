class InRoundaboutState:
    def __init__(self, globals):
        self.globals = globals
        self.name = "InRoundaboutState"

    def run(self):
        self.globals.target_speed = self.globals.max_speed

        print ""
        print "-----------------------------------------"
        print "State: ", self.name
        print "-----------------------------------------"
        print "Roundabout distance: ", self.globals.roundabout.getDistance()