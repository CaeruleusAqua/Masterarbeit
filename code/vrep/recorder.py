#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import threading

import opendavinci.odvdvehicle_pb2 as odvdVehicle
import opendavinci.odvdxc90_pb2 as odvdXC90
import opendavinci.automotivedata_pb2 as automotive
from mpc_model import OdeModel
from opendavinci.DVnode import DVnode
from tools import Rate
from tools import getch
import math

filename = sys.argv[1]


node = DVnode(cid=216)

def callback(container):
    global node, filename
    print container
    node.writeToFile(container,filename)



node.registerContainerCallback(callback)
node.connect()

node.spin()