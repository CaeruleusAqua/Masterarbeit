class ScenarioImage:
    def __init__(self):
        self.name = "Image"
        self.file = None
        self.originx = 0
        self.originy = 0
        self.mppx = 1
        self.mppy = 1
        self.rotz = 0

    def getLines(self):
        endl = "\n"
        s = str(self.name) + endl
        s += "IMAGE " + str(self.file) + endl
        s += "ORIGINX " + str(self.originx) + endl
        s += "ORIGINY " + str(self.originy) + endl
        s += "MPPX " + str(self.mppx) + endl
        s += "MPPY " + str(self.mppy) + endl
        s += "ROTZ " + str(self.rotz) + endl
        return s
