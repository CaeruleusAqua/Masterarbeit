class Lane:
    def __init__(self, inner_r , outer_r, type):
        self.inner_r = inner_r
        self.outer_r = outer_r
        assert type == "p" or type == "b" or type == "c"
        self.type = type
        self.r = (inner_r + outer_r)/2.0