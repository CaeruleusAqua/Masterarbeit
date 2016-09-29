#!/usr/bin/env python2
import pygame
import sys
import math

from roundabout import junction
from roundabout.junction import Junction
from roundabout.lane import Lane
from roundabout.drawer import Drawer
from roundabout.roundabout import Roundabout

pygame.init()
size = width, height = 800, 800
speed = [2, 2]
black = 0, 0, 0
screen = pygame.display.set_mode(size)
bibliothek = pygame.image.load("images/bibliothek.png")
imagerect = bibliothek.get_rect()
WHITE = (255,255,255)
PI=math.pi
junctions = list()


# junctions.append(Junction([20, 40]))
# junctions.append(Junction([40, 20]))
# junctions.append(Junction([60, 40]))
# junctions.append(Junction([40, 60]))
#
# junctions[0].connect(junctions[1],Lane())
# junctions[1].connect(junctions[2],Lane())
# junctions[2].connect(junctions[3],Lane())
# junctions[3].connect(junctions[0],Lane())


circ = Roundabout([50,100])
circ.add_junktion(0,20)
circ.add_junktion(PI,20)
circ.add_junktion(PI/2,20)
circ.add_junktion(PI*1.5,20)
circ.chain()



drawer = Drawer(screen,4)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    #pygame.draw.circle(screen,white,(160,120),10)
    #pygame.draw.arc(screen, WHITE, [200, 200, 400, 400], 0, 2*PI+1, 2)
    #pygame.draw.arc(screen, WHITE, [300, 300, 200, 200], 0, 2 * PI + 1, 2)
    #screen.blit(bibliothek,(0,0),(90,0,30,116))
    for junk in junctions:
        drawer.draw(junk)
        for lane in junk.lanes:
            drawer.draw(lane)

    drawer.draw(circ)


    #screen.fill(black)
    pygame.time.wait(10)
    pygame.display.flip()
