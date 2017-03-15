#!/usr/bin/env python2
from math import *

import matplotlib
import matplotlib.pyplot as plt

rays=[]
for i in range(-15,0,2):
    rays.append([tan(radians(i))*x+2.1 for x in range(100)])

import random
import matplotlib.pyplot as plt


fig = plt.figure()
ax1 = fig.add_subplot(311)
ax2 = fig.add_subplot(312)
ax3 = fig.add_subplot(313)

for ray in rays:
    ax1.plot(ray)
    ax2.plot(ray)
    ax3.plot(ray)

ax1.set_aspect('equal')
ax2.set_aspect('equal')
ax3.set_aspect('equal')
ax1.axis([0, 25, 0, 2.5])
ax2.axis([25, 50, 0, 2.5])
ax3.axis([50, 75, 0, 2.5])


# Set common labels
fig.text(0.5, 0.04, 'range[m]', ha='center', va='center')
fig.text(0.06, 0.5, 'height[m]', ha='center', va='center', rotation='vertical')

#ax1.set_title('ax1 title')

fig = matplotlib.pyplot.gcf()
fig.set_size_inches(20.5, 8)
fig.savefig('foo.png',dpi=400)
#plt.show()
#plt.savefig('common_labels_text.png', dpi=300)


# for ray in rays:
#     plt.plot(ray)
# plt.ylabel('height[m]')
# plt.xlabel('range[m]')
# plt.axes().set_aspect('equal')
# plt.axis([0, 25, 0, 2.5])
#
# fig = matplotlib.pyplot.gcf()
# fig.set_size_inches(20.5, 5.5)
# fig.savefig('foo.png',dpi=300)
# #plt.show()
#
#
# f, axarr = plt.subplots(2, 2)
# for ray in rays:
#     axarr[0, 0].plot(ray)
#     #axarr[0, 0].ylabel('height[m]')
#     #axarr[0, 0].xlabel('range[m]')
#     axarr[0, 0].axes().set_aspect('equal')
#     axarr[0, 0].axes().axis([0, 25, 0, 2.5])
#
#     axarr[0, 1].plot(ray)
#     #axarr[0, 1].ylabel('height[m]')
#     #axarr[0, 1].xlabel('range[m]')
#     axarr[0, 1].axes().set_aspect('equal')
#     axarr[0, 1].axes().axis([0, 25, 0, 2.5])
#
#     axarr[0, 0].plot(ray)
#     #axarr[0, 0].ylabel('height[m]')
#     #axarr[0, 0].xlabel('range[m]')
#     axarr[0, 0].axes().set_aspect('equal')
#     axarr[0, 0].axes().axis([0, 25, 0, 2.5])
#
#
# plt.show()
#
# # Fine-tune figure; hide x ticks for top plots and y ticks for right plots
# plt.setp([a.get_xticklabels() for a in axarr[0, :]], visible=False)
# plt.setp([a.get_yticklabels() for a in axarr[:, 1]], visible=False)