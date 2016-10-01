import cv2

import state_start
from objects import *
from state import State


class SurfaceDefinitionState(State):
    def __init__(self, globals):
        super(SurfaceDefinitionState, self).__init__(globals)
        self.current_nodes = list()

    def mouse_event(self, event, x, y):
        self.enableHover(self.globals.graph.getNodeAt(x, y))
        if event == cv2.EVENT_LBUTTONDOWN:
            if self.snapy_node:
                tmp = Node((self.snapy_node.pos))
            else:
                tmp = Node((x, y))

            self.globals.drawable.nodes.append(tmp)
            self.current_nodes.append(tmp)
            if len(self.current_nodes) == 4:
                self.globals.drawable.surfaces.append(Surface(self.current_nodes))
                self.globals.graph.nodes+=self.current_nodes
                self.current_nodes = list()


    def keyboard_event(self, key):
        if key == 10:
            self.globals.state = state_start.StartState(self.globals)

    def overlay_event(self):
        # self.globals.overlay.writeLine(2, "Node Id: %s, Node Type; " % (self.node.id))
        self.globals.overlay.writeLine(0, 'Press: "ENTER" to exit Mode, "c" for connect')
