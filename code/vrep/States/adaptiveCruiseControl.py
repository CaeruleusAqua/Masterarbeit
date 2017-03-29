import States


class AdaptiveCruiseControl:
    def __init__(self, globals):
        self.globals = globals
        self.name = "AdaptiveCruiseControl"
        self.intialSpeed = self.globals.speed

    def run(self):
        mypos = self.globals.car.getPosition() * 10
        line_segments = self.globals.parser.scenario.getLineSegments(mypos)
        print "Roadname: ", line_segments[-1][0].parent.parent.name
        print ""
        print "-----------------------------------------"
        print "State: \033[1;33m" + str(self.name) + "\033[0m"
        print "-----------------------------------------"
        print "Roundabout distance: ", self.globals.roundabout.getDistance()
        print "MyCar Speed: ", self.globals.speed

        if len(line_segments) > 0:
            if line_segments[-1][0].parent.parent.name == "South":
                self.globals.currentState = States.ToRoundabout(self.globals)

            is_neart_to_exit = False
            if line_segments[-1][0].parent.parent.name == "Roundabout":
                for segment in line_segments:
                    if segment[0].index > 28 or segment[0].index < 33:
                        self.globals.currentState = States.DriveOutRoundabout(self.globals)
                        self.globals.currentState.run()
