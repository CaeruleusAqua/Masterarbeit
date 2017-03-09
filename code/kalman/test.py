#!/bin/env python2

import random

import matplotlib.pyplot as plt
import numpy as np

from obstacle import Obstacle

obst = Obstacle(0, 0)
dt = 0.1

# generate Measurements
m = 20  # Measurements
vx = 20  # in X
vy = 10  # in Y

x_p = list()
y_p = list()
x_p.append(0)
y_p.append(0)
for n in range(m - 1):
    x_p.append(x_p[-1] + vx * dt)
    y_p.append(y_p[-1] + vy * dt)

for n in range(1, m):
    x_p[n] = x_p[n] + random.random()
    y_p[n] = y_p[n] + random.random()

x_p = np.asarray(x_p)
y_p = np.asarray(y_p)

mx = np.array(vx + np.random.randn(m))
my = np.array(vy + np.random.randn(m))

measurements = np.vstack((x_p, y_p, mx, my))

print(measurements.shape)

print('Standard Deviation of Acceleration Measurements=%.2f' % np.std(mx))
print('You assumed %.2f in R.' % obst.R[0, 0])

# Preallocation for Plotting
xt = []
yt = []

for n in range(len(measurements[0])):
    obst.predict(dt)
    obst.correct(np.asarray([x_p[n], y_p[n], mx[n], my[n]]).reshape(4, 1))
    x = obst.x[0]
    y = obst.x[1]

    print obst.x
    # Save states for Plotting
    xt.append(x)
    yt.append(y)

fig = plt.figure(figsize=(16, 16))
# plt.scatter(xpd, ypd, s=20, label='predict', c='y')
plt.scatter(x_p, y_p, s=20, label='Real', c='b')
plt.scatter(xt, yt, s=20, label='State', c='k')
plt.scatter(xt[0], yt[0], s=100, label='Start', c='g')
plt.scatter(xt[-1], yt[-1], s=100, label='Goal', c='r')

plt.xlabel('X')
plt.ylabel('Y')
plt.title('Position')
plt.legend(loc='best')
plt.axis('equal')
plt.show()
