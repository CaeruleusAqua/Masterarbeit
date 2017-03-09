import math

import numpy as np

from remoteApi import vrep
from remoteApi import vrepConst


class VrepObject(object):
    def __init__(self, clientID, name):
        self.clientID = clientID
        self.name = name
        self.handle = vrep.simxGetObjectHandle(self.clientID, name, vrepConst.simx_opmode_blocking)[1]
        self.pos = None
        self.theta = None

    def getPosition(self):
        return np.array(self.pos)

    def getOriantation(self):
        return np.array(self.theta)


    def getDistance(self):
        return math.sqrt(self.pos[0] * self.pos[0] + self.pos[1] * self.pos[1] + self.pos[2] * self.pos[2])

    def update(self, reference):
        if self.pos == None:
            self.pos = vrep.simxGetObjectPosition(self.clientID, self.handle, reference, vrepConst.simx_opmode_streaming)[1]
        else:
            self.pos = vrep.simxGetObjectPosition(self.clientID, self.handle, reference, vrepConst.simx_opmode_buffer)[1]

        if self.theta == None:
            self.theta = vrep.simxGetObjectOrientation(self.clientID, self.handle, reference, vrepConst.simx_opmode_streaming)[1]
        else:
            self.theta = vrep.simxGetObjectOrientation(self.clientID, self.handle, reference, vrepConst.simx_opmode_buffer)[1]

    def setPosition(self, pos, relative):
        vrep.simxSetObjectPosition(self.clientID, self.handle, relative, pos, vrepConst.simx_opmode_oneshot)
