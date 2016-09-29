#!/usr/bin/env python2
import matplotlib.pyplot as plt
import numpy as np
import xml.etree.ElementTree as ET
from math import log, tan, atan,exp, pi as PI

fig = plt.figure()

##http://stackoverflow.com/questions/1185408/converting-from-longitude-latitude-to-cartesian-coordinates




earth_radius = 6378137


def deg2rad(d):
    return (((d) * PI) / 180.0)


def rad2deg(d):
    return (((d) * 180.0) / PI)



def y2lat_m(y):
    return rad2deg(2 * atan(exp((y / earth_radius))) - PI / 2)


def x2lon_m(x):
    return rad2deg(x / earth_radius)


def lat2y_m(lat):
    return earth_radius * log(tan(PI / 4 + deg2rad(lat) / 2))


def lon2x_m(lon):
    return deg2rad(lon) * earth_radius


tree = ET.parse('test.osm')
root = tree.getroot()
x = list()
y = list()

i = 0
for child in root:
    i += 1
    if child.tag == "node":
        lon = float(child.attrib['lon'])
        lat = float(child.attrib['lat'])
        x.append(lon2x_m(lon))
        y.append(lat2y_m(lat))

plt.plot(x, y, 'ro')
plt.axes().set_aspect('equal', 'datalim')


plt.show()
