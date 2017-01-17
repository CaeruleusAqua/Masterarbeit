#!/usr/bin/env python2
import pickle
import matplotlib.pyplot as plt
from tools import gps
import numpy as np
from scipy.optimize import minimize
from tools import WGS84Coordinate


(lat,lon) = pickle.load( open( "gps.p", "rb" ) )
low_bound = 3600
upp_bound = 11000


roundabout_lon = np.mean(lon[low_bound:upp_bound])
roundabout_lat = np.mean(lat[low_bound:upp_bound])

trans = WGS84Coordinate(roundabout_lat,roundabout_lon)

points = list()
for i in xrange(low_bound, upp_bound):
    points.append(trans.transformToCart(lat[i],lon[i]))

#print points




circle0 = plt.Circle((0, 0), 15, color='b')
circle1 = plt.Circle((0, 0), 5, color='r')


fig, ax = plt.subplots()

ax.add_artist(circle0)
ax.add_artist(circle1)

fig.show()
q = list()
w = list()
for point in points:
    q.append(point[0])
    w.append(point[1])


plt.plot(q,w,'ro')
ax.set_aspect('equal', 'datalim')
plt.show()
