#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from opendavinci.DVnode import DVnode
from opendavinci import automotivedata_pb2

filename = sys.argv[1]

node = DVnode(cid=216)


def callback(container):
    global node, filename
    node.writeToFile(container, filename)
    if container.dataType == 19:
        msg = automotivedata_pb2.geodetic_WGS84()
        msg.ParseFromString(container.serializedData)
        print msg


node.registerContainerCallback(callback)
node.connect()

node.spin()
