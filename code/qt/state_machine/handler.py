import cv2

from objects import *
from parser import JsonHandler
from start import StartState
from add_node import AddNodeState


class StateHandler:
    def __init__(self, file):
        self.mode = 0
        self.step = 0
        self.parser = JsonHandler()
        self.graph = Graph()

        self.file = open(file, 'r+')

        self.mark = None
        self.elem = None
        self.snapy = None
        self.updated = True
        self.overlay = None
        self.cursor_pos = None

        self.state = AddNodeState(self)
        self.info = None

    def update(self):
        tmp = self.updated
        self.updated = False
        return tmp

    def mouse_event(self, event, x, y):
        self.state.mouse_event(event, x, y)



    def keyboard_event(self, key):
        self.state.keyboard_event(key)
        self.updated = True

    def overlay_event(self):
        self.state.overlay_event()

    def shutdown(self):
        self.file.close()
