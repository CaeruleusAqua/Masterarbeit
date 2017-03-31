#!/usr/bin/env python2

import math
import time
import numpy as np
import pickle
import pylab

import matplotlib.pyplot as plt


measurements = pickle.load(open("measurements.p", "rb"))    #[self.globals.iteration, self.pos, self.speed, self.theta, self.type]
simulation = pickle.load(open("simulation.p", "rb"))        #[self.iteration, enemy.getPosition(), enemy.speed, enemy.getOriantation(), enemy.type]


print measurements.keys()
print simulation.keys()

mapping= dict()

for sim_key in simulation.keys():
    mapping[sim_key] = list()

## map measurements_to_sim

for key in measurements.keys():
    data = measurements[key][0]
    time = data[0]
    for sim_key in simulation.keys():
        dist = np.linalg.norm(np.array(data[1])- np.array(simulation[sim_key][time][1]))
        if dist < 0.3:
            mapping[sim_key].append(key)
            break






print mapping


for sim_key in simulation.keys():
    print sim_key

    for mess in mapping[sim_key]:
        times= list()
        distances = list()

        for data in measurements[mess]:
            dist = np.linalg.norm(np.array(data[1]) - np.array(simulation[sim_key][data[0]][1]))
            times.append(data[0])
            distances.append(dist)

        pylab.plot(times,distances,label=str(mess))
    pylab.ylabel(str(sim_key))
    pylab.legend(loc='upper left')
    pylab.show()