import pygame


class Lane:
    def __init__(self):
        self.speed = 30
        self.color = (255, 255, 255)
        self.width = 10
        self.junctions = list()

    def get_length(self):
        pass