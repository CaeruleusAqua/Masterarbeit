#!/bin/env python2

from math import sin, cos

import matplotlib.pyplot as plt
import numpy as np

from obstacle import Obstacle

obst = Obstacle(0, 0)
dt = 0.1

# generate Measurements
m = 200  # Measurements
vx = 20  # in X
vy = 10  # in Y

v = 20
yaw = 0.1

x = list()
y = list()
vel = list()
theta = list()
yawrate = list()
x_vel = list()
y_vel = list()

x.append(0)
y.append(0)
vel.append(v)
theta.append(0)
yawrate.append(yaw)
x_vel.append(0)
y_vel.append(0)

for n in range(1, m):
    if n == m / 2:
        yaw = -yaw * 2
    x.append(x[-1] + vel[-1] * cos(theta[-1]) * dt)
    y.append(y[-1] + vel[-1] * sin(theta[-1]) * dt)
    theta.append(theta[-1] + yawrate[-1] * dt)
    yawrate.append(yaw)
    vel.append(v)
    x_vel.append((x[-1] - x[-2]) / dt)
    y_vel.append((y[-1] - y[-2]) / dt)

x = np.array(x + np.random.randn(m) * 1)
y = np.array(y + np.random.randn(m) * 1)
x_vel = np.array(x_vel + np.random.randn(m) * 0.1)
y_vel = np.array(y_vel + np.random.randn(m) * 0.1)

measurements = np.vstack((x, y, x_vel, y_vel))

print(measurements.shape)

print('Standard Deviation of Acceleration Measurements=%.2f' % np.std(x))
print('You assumed %.2f in R.' % obst.R[0, 0])

# Preallocation for Plotting
xt = []
yt = []

for n in range(len(measurements[0])):
    obst.predict(dt)
    obst.correct(np.asarray([x[n], y[n], x_vel[n], y_vel[n]]).reshape(4, 1))
    x_tmp = obst.x[0]
    y_tmp = obst.x[1]

    # Save states for Plotting
    xt.append(x_tmp)
    yt.append(y_tmp)

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
