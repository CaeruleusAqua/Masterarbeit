class Lane:
    def __init__(self, inner_r , outer_r, type, debug_marker):
        self.inner_r = inner_r
        self.outer_r = outer_r
        assert type == "p" or type == "b" or type == "c"
        self.type = type
        self.r = (inner_r + outer_r)/2.0
        self.intersection_position = None
        self.lineSegment = None
        self.posInLineSegment = 0
        self.debug = debug_marker