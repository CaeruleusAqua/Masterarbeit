#!/usr/bin/env python2

import math
import time
import numpy as np
import pickle
import pylab

import matplotlib.pyplot as plt

measurements = pickle.load(open("measurements.p", "rb"))  # [self.globals.iteration, self.pos, self.speed, self.theta, self.type]
simulation = pickle.load(open("simulation.p", "rb"))  # [self.iteration, enemy.getPosition(), enemy.speed, enemy.getOriantation(), enemy.type]

simulation["Car0"] = simulation.pop("enemy_car1")
simulation["Car1"] = simulation.pop("enemy_car2")
simulation["Car2"] = simulation.pop("enemy_car3")
simulation["Bike2"] = simulation.pop("bike")
simulation["Pedestrian"] = simulation.pop("Bill_base")

print measurements.keys()
print simulation.keys()

print "Simulation Time: ",len(simulation["Car2"])/10
pylab.rc('font',**{'family':'serif','serif':['Computer Modern Roman']})
pylab.rc('text', usetex=True)

mapping = dict()

for sim_key in simulation.keys():
    mapping[sim_key] = list()

## map measurements_to_sim

for key in measurements.keys():
    data = measurements[key][0]
    time = data[0]
    for sim_key in simulation.keys():
        dist = np.linalg.norm(np.array(data[1]) - np.array(simulation[sim_key][time][1]))
        if dist < 0.3:
            mapping[sim_key].append(key)
            break



for sim_key in simulation.keys():
    if sim_key != "mycar":
        print ""
        print sim_key
        counter=0
        car = 0
        pedestrian =0
        bicycle = 0
        unknown = 0

        for mess in mapping[sim_key]:
            for data in measurements[mess]:
                #print "Messtype: ",data[4]
                #print "Simtype: ",simulation[sim_key][data[0]][4]
                if data[4] == "p":
                    pedestrian+=1

                elif data[4] == "c":
                    car+=1

                elif data[4] == "b":
                    bicycle += 1

                else:
                    unknown+=1
                counter+=1

        if counter != 0:
            print "Car: ",car / float(counter)
            print "Ped: ",pedestrian / float(counter)
            print "Bike: ",bicycle / float(counter)
            print "unk: ",unknown / float(counter)



for sim_key in simulation.keys():
    if sim_key != "mycar":
        print ""
        print sim_key
        pos_err = 0
        counter = 0

        for mess in mapping[sim_key]:
            times = list()
            distances = list()


            for data in measurements[mess]:
                dist = np.linalg.norm(np.array(data[1][:2]) - np.array(simulation[sim_key][data[0]][1][:2]))*10
                pos_err += dist
                counter+=1
                # print np.array(simulation[sim_key][data[0]][1])




        print "average Position error: ",pos_err / float(counter)
        print "redetects: ",len(mapping[sim_key])
        #pylab.show()





# pylab.figure(num=1, figsize=(4.72441, 4.72441*0.62), facecolor='w', edgecolor='k')
# for sim_key in simulation.keys():
#     if sim_key != "mycar":
#         print sim_key
#
#         for mess in mapping[sim_key]:
#             times = list()
#             distances = list()
#
#
#             for data in measurements[mess]:
#                 dist = np.linalg.norm(np.array(data[1][:2]) - np.array(simulation[sim_key][data[0]][1][:2]))
#                 # print np.array(simulation[sim_key][data[0]][1])
#                 if data[0] < 150:
#                     times.append(data[0] / 10.0)
#                     distances.append(dist * 10)
#             if measurements[mess][0][0] < 150 and len(measurements[mess]) > 2:
#                 pylab.plot(times, distances, label=str(mess),linewidth=0.5)
#
#
#
#         pylab.ylabel("position error [m]")
#         pylab.xlabel("time [s]")
#         pylab.title(str(sim_key))
#         pylab.legend(loc='upper left')
#         pylab.tight_layout()
#         pylab.savefig(str(sim_key)+'_pos_err.pdf')#,bbox_inches='tight')
#         pylab.clf()
#         #pylab.show()

# for sim_key in simulation.keys():
#     if sim_key != "mycar":
#         print sim_key
#
#         for mess in mapping[sim_key]:
#             times = list()
#             distances = list()
#             distances_car = list()
#
#
#             for data in measurements[mess]:
#                 dist = np.linalg.norm(np.array(data[1][:2]) - np.array(simulation[sim_key][data[0]][1][:2]))
#                 car_dist = np.linalg.norm(np.array(data[1][:2]) - np.array(simulation["mycar"][data[0]][1][:2]))
#                 # print np.array(simulation[sim_key][data[0]][1])
#                 if data[0] < 150:
#                     distances_car.append(car_dist *10.0)
#                     distances.append(dist * 10.0)
#             if measurements[mess][0][0] < 150 and len(measurements[mess]) > 2:
#                 #pylab.plot(distances_car, distances,'o' ,label=str(mess),linewidth=0.5)
#                 pylab.scatter(distances_car, distances,label=str(mess),s=0.5)
#
#
#
#         pylab.ylabel("position error [m]")
#         pylab.xlabel("distance to car [m]")
#         pylab.title(str(sim_key))
#         pylab.legend(loc='upper left')
#         pylab.tight_layout()
#         pylab.savefig(str(sim_key)+'_pos_err_dist.pdf')#,bbox_inches='tight')
#         pylab.clf()
#         #pylab.show()
#
#
# for sim_key in simulation.keys():
#     if sim_key != "mycar":
#         print sim_key
#
#         oldpos = None
#         sim_speed = list()
#         times = list()
#         for dat in simulation[sim_key][1:150]:
#             if oldpos is not None:
#                 sim_speed.append(np.linalg.norm(dat[1] - oldpos) * 100)
#                 times.append(dat[0]/10.0)
#             oldpos = dat[1]
#
#         pylab.plot(times, sim_speed, label=str(sim_key),linewidth=0.5)
#
#         for mess in mapping[sim_key]:
#             times = list()
#             speed = list()
#
#             for data in measurements[mess]:
#                 dist = np.array(data[2])  # - np.array(simulation[sim_key][data[0]][2])
#                 if data[0] < 150:
#                     times.append(data[0] / 10.0)
#                     speed.append(dist * 10)
#
#             if measurements[mess][0][0] < 150 and len(measurements[mess]) > 2:
#                 pylab.plot(times, speed, label=str(mess),linewidth=0.5)
#
#
#         pylab.ylabel("speed [m/s]")
#         pylab.xlabel("time [s]")
#         pylab.legend(loc='upper left')
#         pylab.tight_layout()
#         pylab.savefig(str(sim_key)+'._speed.pdf')#,bbox_inches='tight')
#         pylab.clf()
#         #pylab.show()
#
#
# for sim_key in simulation.keys():
#     if sim_key != "mycar":
#         print sim_key
#
#         xval = list()
#         yval = list()
#         for dat in simulation[sim_key][1:150]:
#             xval.append(dat[1][0])
#             yval.append(dat[1][1])
#         pylab.plot(xval, yval, label=str(sim_key),linewidth=0.5)
#
#         for mess in mapping[sim_key]:
#             xval = list()
#             yval = list()
#
#             pylab.axis('equal')
#             for data in measurements[mess]:
#                 dist = np.array(data[2])  # - np.array(simulation[sim_key][data[0]][2])
#                 if data[0] < 100:
#                     xval.append(data[1][0])
#                     yval.append(data[1][1])
#             if measurements[mess][0][0] < 150 and len(measurements[mess]) > 2:
#                 pylab.plot(xval, yval, label=str(mess),linewidth=0.5)
#
#         #pylab.title(str(sim_key))
#         pylab.ylabel("y-pos [m]")  #
#         pylab.xlabel("x-pos [m]")
#         pylab.legend(loc='upper left')
#         pylab.tight_layout()
#         pylab.savefig(str(sim_key) + '_position.pdf')#, bbox_inches='tight')
#         pylab.clf()
#         #pylab.show()
