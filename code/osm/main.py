#!/usr/bin/env python2
import matplotlib.pyplot as plt
import numpy as np
import xml.etree.ElementTree as ET
from math import cos, sin, sqrt, asin, pi as PI
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')


##http://stackoverflow.com/questions/1185408/converting-from-longitude-latitude-to-cartesian-coordinates


def GetSphericalLatitude(GPSLatitude):
    h = 0
    A = 6378137  # semi-major axis
    f = 1 / 298.257223563  # 1/f Reciprocal of flattening
    e2 = f * (2 - f)
    Rc = A / (sqrt(1 - e2 * (sin(GPSLatitude * PI / 180) ** 2)))
    p = (Rc + h) * cos(GPSLatitude * PI / 180)
    z = (Rc * (1 - e2) + h) * sin(GPSLatitude * PI / 180)
    r = sqrt(p ** 2 + z ** 2)
    SphericalLatitude = asin(z / r) * 180 / PI
    return SphericalLatitude


def getCartesian(lat, lon):
    lat = GetSphericalLatitude(lat)
    R = 6371000
    lat = lat* PI / 180
    lon = lon * PI / 180
    x = R * cos(lat) * cos(lon)
    y = R * cos(lat) * sin(lon)
    z = R * sin(lat)
    return np.array([x, y, z])


tree = ET.parse('test.osm')
root = tree.getroot()
first = None
i = 0
for child in root:
    i += 1
    if child.tag == "node" and i % 10 == 3:

        lon = float(child.attrib['lon'])
        lat = float(child.attrib['lat'])
        cart = getCartesian(lat, lon)
        if first is None:
            first = cart
        else:
            diff = cart - first
            ax.scatter(diff[0], diff[1], diff[2], c='r', marker='o')

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

plt.show()
