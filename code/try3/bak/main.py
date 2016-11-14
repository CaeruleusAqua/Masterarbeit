#!/usr/bin/env python2


import math


def getRange(r1, r2, dist):
    print "radius sensor: ", r1
    print "radius kreisverkehr: ", r2
    a = r1
    b = r2
    c = b + dist

    y = (a ** 2 + c ** 2 - b ** 2) / (2 * c)
    x = math.sqrt(a ** 2 - y ** 2)

    print y

    sehne = x * 2
    a = 2 * (math.asin(sehne / (2 * b))) / 2
    if y > b:
        a = ((math.pi/2) - a)+math.pi/2

    print (a / math.pi) * 180
    dist = a / (math.pi * 2) * math.pi * 2 * b
    return dist


d = 20.0  # # durchmesser kreisverkehr
srange = 20  # sensor reichweite

accel = 2  # m/ss
v_max = 20 / 3.6  # m/s

frange = getRange(srange, d / 2.0, 0)
print "Entfernung Fahrzeug:", frange
atime=frange/v_max
print "Zeit bis ankunft:", atime
print "zeit zum erreichen von v_max: ", v_max/accel
