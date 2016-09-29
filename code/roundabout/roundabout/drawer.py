import pygame

from junction import Junction
from lane import Lane
from ark import Ark
from roundabout import Roundabout
import numpy as np


class Drawer:
    def __init__(self, screen, scale):
        self.scale = scale
        self.screen = screen

    def draw(self, obj):
        if isinstance(obj, Junction):
            pygame.draw.circle(self.screen, (255, 0, 0), map(int,obj.pos * self.scale), 10)

        elif isinstance(obj, Lane):
            pygame.draw.line(self.screen, (255, 0, 255), obj.junctions[0].pos * self.scale, obj.junctions[1].pos * self.scale, obj.width * self.scale)

        elif isinstance(obj, Ark):
            box=[obj.center[0]-obj.radius,obj.center[1]-obj.radius,2*obj.radius,2*obj.radius]
            box=np.array(box)*self.scale
            pygame.draw.arc(self.screen, (255, 0, 255),box, obj.start, obj.end, obj.width)

        elif isinstance(obj, Roundabout):
            pygame.draw.circle(self.screen, (0, 255, 0), obj.pos * self.scale, 10)
            for angle in obj.junctions.keys():
                self.draw(obj.junctions[angle])
                for lane in obj.junctions[angle].lanes:
                    self.draw(lane)


        else:
            raise NotImplementedError("Object Type\'" + str(obj.__class__) + "\' is not drawable")
