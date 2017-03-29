import numpy as np
from math import atan2, cos, sin


class LineSegment:
    def __init__(self, p, q, parent, precursor,index):
        self.index= index
        self.precursor = precursor
        self.successor = None
        self.parent = parent
        if precursor is not None:
            precursor.successor = self

        # berechnung aus der Nomalenform
        self.start = p[:2]
        self.end = q[:2]
        self.length = np.linalg.norm(self.start - self.end)
        self.normal = np.array([-(self.end[1] - self.start[1]), self.end[0] - self.start[0]])
        if np.dot(self.start, self.normal) >= 0:
            self.normal = self.normal / np.linalg.norm(self.normal)
        else:
            self.normal = -self.normal / np.linalg.norm(self.normal)

        #calculate rectangle extension
        self.angle = None
        self.distance = np.dot(self.start, self.normal)
        self.extension = 0
        if precursor is not None:
            a = precursor.start - precursor.end
            b = self.end - self.start
            skalar_prod = np.dot(a, b)
            self.angle = np.arccos(skalar_prod / (np.linalg.norm(a) * np.linalg.norm(b)))
            self.extension = np.tan(np.pi-self.angle) * (self.parent.width / 2)
            #print "Segment Extension: ", self.extension

    def getDist(self, p):
        point = p[:2]
        return np.dot(point, self.normal) - self.distance

    def isInSegment(self, p):
        point = p[:2]
        ## rotation und translation, start is origin
        new_end = self.end - self.start
        theta = atan2(new_end[1], new_end[0])
        rot = np.array([[cos(theta), sin(theta)], [-sin(theta), cos(theta)]])
        endx = np.matmul(rot, new_end)[0]
        proj_point = np.matmul(rot, point - self.start)
        if proj_point[0] >= -self.extension and proj_point[0] <= endx:
            if abs(proj_point[1]) < self.parent.width / 2:
                return proj_point[0]
        return False

        # # to many special cases if origin is in line segment!
        # point = p[:2]
        # if abs(self.getDist(point)) <= self.parent.width / 2:
        #     border_normal = self.end - self.start
        #     if np.dot(self.start, border_normal) >= 0:
        #         start_normal = border_normal / np.linalg.norm(border_normal)
        #     else:
        #         start_normal = -border_normal / np.linalg.norm(border_normal)
        #
        #     if np.dot(self.end, border_normal) >= 0:
        #         end_normal = border_normal / np.linalg.norm(border_normal)
        #     else:
        #         end_normal = -border_normal / np.linalg.norm(border_normal)
        #
        #     distance_start = np.dot(self.start, start_normal)
        #     distance_end = np.dot(self.end, end_normal)
        #     #print self.parent.parent.name
        #     #print point
        #     #print distance_start
        #     #print distance_end
        #     if np.sign(np.dot(point, start_normal) - distance_start) != np.sign(np.dot(point, end_normal) - distance_end):
        #         print self.parent.parent.name
        #         print abs(self.getDist(point))
        #         print "Dist start : ",np.dot(point, start_normal) - distance_start
        #         print "Dist end   : ",np.dot(point, end_normal) - distance_end
        #         print self.start
        #         print self.end
        #
        #
        #         return True
        #
        # return False
