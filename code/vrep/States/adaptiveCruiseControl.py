
class AdaptiveCruiseControl:
    def __init__(self, globals):
        self.globals = globals
        self.name = "AdaptiveCruiseControl"
        self.intialSpeed = self.globals.speed

    def run(self):
        print ""
        print "-----------------------------------------"
        print "State: \033[1;33m" + str(self.name) + "\033[0m"
        print "-----------------------------------------"
        print "Roundabout distance: ", self.globals.roundabout.getDistance()
        print "MyCar Speed: ", self.globals.speed


