import States


class AdaptiveCruiseControl:
    def __init__(self, globals):
        self.globals = globals
        self.name = "AdaptiveCruiseControl"
        self.intialSpeed = self.globals.speed

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

        if len(line_segments) > 0:
            for segment in line_segments:
                if segment[0].parent.parent.name == "Roundabout":
                    print "Segment Index: ", segment[0].index
                    if segment[0].index > 28 and segment[0].index < 33:
                        self.globals.currentState = States.DriveOutRoundabout(self.globals)
                        return
