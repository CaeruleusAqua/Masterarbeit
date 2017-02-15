import numpy as np


class LineSegment:
    def __init__(self, p, q, width):

        # berechnung aus der Nomalenform
        self.width = width
        self.start = p
        self.end = q
        self.length = np.linalg.norm(p - q)
        self.normal = np.array([-(q[1] - p[1]), q[0] - p[0]])
        if np.dot(p, self.normal) >= 0:
            self.normal = self.normal / np.linalg.norm(self.normal)
        else:
            self.normal = -self.normal / np.linalg.norm(self.normal)
        self.distance = np.dot(p, self.normal)

    def getDist(self, p):
        return np.dot(p, self.normal) - self.distance

    def isInSegment(self, p):
        if self.getDist(p) <= self.width / 2:
            border_normal = self.end - self.start
            if np.dot(self.start, border_normal) >= 0:
                start_normal = border_normal / np.linalg.norm(border_normal)
            else:
                start_normal = -border_normal / np.linalg.norm(border_normal)

            if np.dot(self.end, border_normal) >= 0:
                end_normal = border_normal / np.linalg.norm(border_normal)
            else:
                end_normal = -border_normal / np.linalg.norm(border_normal)

            distance_start = np.dot(self.start, start_normal)
            distance_end = np.dot(self.end, end_normal)
            if np.sign(np.dot(p, start_normal) - distance_start) != np.sign(np.dot(p, end_normal) - distance_end):
                return True

        return False
