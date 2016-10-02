from objects import *
from parser import JsonHandler
from state_start import StartState


class StateHandler:
    def __init__(self, file):

        self.graph = ObjectContainer()
        self.drawable = DrawableContainer()

        self.mark = None
        self.snapy = None
        self.updated = True
        self.overlay = None

        self.state = StartState(self)

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
