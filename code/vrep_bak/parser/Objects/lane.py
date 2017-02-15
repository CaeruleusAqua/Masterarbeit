class Lane:
    def __init__(self):
        self.id = None
        self.width = None
        self.lanemarking_right = None
        self.lanemarking_left = None
        self.pointmodel = []
        self.parent = None
        self.connections = []
        self.connections_str = []
        self.driving_direction = []

    class LaneMarking:
        DOUBLE_YELLOW = "double_yellow"
        SOLID_YELLOW = "solid_yellow"
        SOLID_WHITE = "solid_white"
        BROKEN_WHITE = "broken_white"
        CROSSWALK = "crosswalk"

    class LaneType:
        CAR = "car"
        PEDESTRIAN = "ped"
        BICYCLE = "bicycle"
