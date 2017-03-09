#!/usr/bin/env python2

from tools import WGS84Coordinate


trans = WGS84Coordinate(57.772840, 12.769964)

pos = [1, 1]
print "Position: ", pos
wgs84_pos = trans.transformToWGS84XY(pos[0], pos[1])
print "Position_trans: ", trans.transformToCart(wgs84_pos.getLatitude(), wgs84_pos.getLongitude())
print "Lat: ", wgs84_pos.getLatitude()
print "Lon: ", wgs84_pos.getLongitude()