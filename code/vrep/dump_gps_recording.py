#!/usr/bin/env python2
import pickle
import struct
import sys

import matplotlib.pyplot as plt

import opendavinci.automotivedata_pb2 as auto
import opendavinci.opendavinci_pb2 as od
from tools import gps

if len(sys.argv) < 2:
    print "\033[1;31;40mError: Missing Parameters, minimum number of parameter is 1 \033[0;37;40m"
    print "Usage: "
    print "       $ protoPrint.py input.rec "
    print ""
    sys.exit(234)

x = list()
y = list()
lat = list()
lon = list()


# Print Container's content.
def printContainer(c):
    # print "Container ID = " + str(c.dataType)
    if c.dataType == 19:
        msg = auto.geodetic_WGS84()
        msg.ParseFromString(c.serializedData)
        x.append(gps.lat2y_m(msg.latitude))
        y.append(gps.lon2x_m(msg.longitude))
        lat.append(msg.latitude)
        lon.append(msg.longitude)
        # print msg


# Read contents from file.
with open(sys.argv[1], "rb") as f:
    print "Reading File, please wait.."

    buf = ""
    bytesRead = 0
    expectedBytes = 0
    LENGTH_OPENDAVINCI_HEADER = 5
    consumedOpenDaVINCIContainerHeader = False

    byte = f.read(1)
    while byte != "":
        buf = buf + byte
        bytesRead = bytesRead + 1

        if consumedOpenDaVINCIContainerHeader:
            expectedBytes = expectedBytes - 1
            if expectedBytes == 0:
                container = od.odcore_data_MessageContainer()
                container.ParseFromString(buf)
                printContainer(container)
                # sys.exit()
                # time.sleep(0.1)
                # Start over and read next container.
                consumedOpenDaVINCIContainerHeader = False
                bytesRead = 0
                buf = ""

        if not consumedOpenDaVINCIContainerHeader:
            if bytesRead == LENGTH_OPENDAVINCI_HEADER:
                consumedOpenDaVINCIContainerHeader = True
                byte0 = buf[0]
                byte1 = buf[1]
                # Check for OpenDaVINCI header.
                if ord(byte0) == int('0x0D', 16) and ord(byte1) == int('0xA4', 16):
                    v = struct.unpack('<L', buf[1:5])  # Read uint32_t and convert to little endian.
                    expectedBytes = v[0] >> 8  # The second byte belongs to OpenDaVINCI's Container header.
                    buf = ""  # Reset buffer as we will read now the actual serialized data from Protobuf.
                else:
                    print "Failed to consume OpenDaVINCI container."

        # Read next byte.
        byte = f.read(1)

pickle.dump((lat, lon), open("gps.p", "wb"))

fig = plt.figure()
plt.plot(x, y, 'ro')
plt.axes().set_aspect('equal', 'datalim')
plt.show()
