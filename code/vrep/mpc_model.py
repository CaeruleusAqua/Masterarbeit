#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  9 16:00:24 2014
@author: jayf
"""
import math

import matplotlib.pyplot as plt
import numpy as np


class OdeModel:
    def __init__(self):
        # Physikalische Eigenschaften
        self.L = 2.2570  # [m] Gesamtlaenge des Radstandes   *nicht ueberprueft*

        # x0 : y global
        # x1 : x global
        # x2 : heading

    def solve(self, x_start, u, n_steps, dt):
        # stores solutions
        xs = np.zeros(shape=(n_steps + 1, 4))
        # set starting condition
        xs[0, :] = x_start
        # solve
        for i in xrange(1, n_steps + 1):
            xs[i, :] = np.array(self.f_discrete(xs[i - 1, :], dt, u))

        return xs

    def f_discrete(self, x, delta_t, u):
        # i2 = x-axis
        # i1 = y-axis
        # i2 = theta
        # i3 = velocity

        x0 = x[0] + x[3] * math.cos(x[2]) * delta_t
        x1 = x[1] + x[3] * math.sin(x[2]) * delta_t
        x2 = x[2] + ((x[3] / self.L) * math.tan(u)) * delta_t
        x3 = x[3]

        return [x0, x1, x2, x3]




# model = OdeModel()
# track = model.solve([0, 0, 0, 10], 0.1, 100, 0.01)
#
# plt.plot(track[:, 1], track[:, 0])
# plt.axis('equal')
# plt.ylabel('some numbers')
# plt.show()
#
# print track[:, 0]
