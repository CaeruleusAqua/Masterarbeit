#!/bin/env python2

from math import sin, cos

import matplotlib.pyplot as plt
import numpy as np

from obstacle_yaw import Obstacle

dt = 0.1

# generate Measurements
m = 250  # Measurements
v = 20
yaw = 0.2

obst = Obstacle(0, 0, 0, v, yaw)

x = list()
y = list()
vel = list()
theta = list()
yawrate = list()

x.append(0)
y.append(0)
vel.append(v)
theta.append(0)
yawrate.append(yaw)

for n in range(1, m):
    # if n == m / 2:
    #     yaw = -yaw * 2
    x.append(x[-1] + vel[-1] * cos(theta[-1]) * dt)
    y.append(y[-1] + vel[-1] * sin(theta[-1]) * dt)
    theta.append(theta[-1] + yawrate[-1] * dt)
    yawrate.append(yaw)
    vel.append(v)

x = np.array(x + np.random.randn(m) * 0.2)
y = np.array(y + np.random.randn(m) * 0.2)
yawrate = np.array(yawrate + 0.1 * np.random.randn(m))
vel = np.array(vel + 0.1 * np.random.randn(m))
theta = np.array(theta + 0.1 * np.random.randn(m))
# yawrate = np.array(yawrate*np.zeros(m))
# vel = np.array(vel*np.zeros(m))




measurements = np.vstack((x, y, vel, yawrate))

print(measurements.shape)

print('Standard Deviation of Acceleration Measurements=%.2f' % np.std(vel))
print('You assumed %.2f in R.' % obst.R[0, 0])

# Preallocation for Plotting
xt = []
yt = []

i = 0

for n in range(len(measurements[0])):
    # if i%10 == 0:
    obst.predict(dt)
    bounded_theta = (theta[n] + np.pi) % (2.0 * np.pi) - np.pi
    obst.correct(np.asarray([x[n], y[n],bounded_theta, vel[n], yawrate[n]]))
    xm = float(obst.x[0])
    ym = float(obst.x[1])
    # print xm, ym
    # print yawrate[n]


    # Save states for Plotting
    xt.append(xm)
    yt.append(ym)
    i += 1

print len(xt)

fig = plt.figure(figsize=(16, 16))
# plt.scatter(xpd, ypd, s=20, label='predict', c='y')
plt.scatter(x, y, s=20, label='Real', c='b')
plt.scatter(xt, yt, s=20, label='State', c='k')
plt.scatter(xt[0], yt[0], s=100, label='Start', c='g')
plt.scatter(xt[-1], yt[-1], s=100, label='Goal', c='r')

plt.xlabel('X')
plt.ylabel('Y')
plt.title('Position')
plt.legend(loc='best')
plt.axis('equal')
plt.show()
