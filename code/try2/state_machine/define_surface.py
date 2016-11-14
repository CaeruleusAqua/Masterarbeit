import cv2

import state_start
from objects import *
from state import State


class SurfaceDefinitionState(State):
    def __init__(self, globals):
        super(SurfaceDefinitionState, self).__init__(globals)
        self.current_nodes = list()
        borders = list()

    def mouse_event(self, event, x, y):
        self.enableHover(self.globals.graph.getNodeAt(x, y))
        if event == cv2.EVENT_LBUTTONDOWN:
            if self.snapy_node:
                tmp = self.snapy_node
            else:
                tmp = Node((x, y))

            self.globals.graph.nodes.append(tmp)
            self.current_nodes.append(tmp)
            if len(self.current_nodes) == 4:
                nodes = self.current_nodes
                borders = [Border(nodes[0], nodes[1]), Border(nodes[1], nodes[2]), Border(nodes[2], nodes[3]), Border(nodes[3], nodes[0])]
                self.globals.graph.borders += borders
                surface =Surface(borders)
                self.globals.graph.surfaces.append(surface)
                self.globals.graph.nodes += self.current_nodes
                self.globals.graph.nodes.append(surface.getAnchor())
                self.current_nodes = list()

    def keyboard_event(self, key):
        if key == 10:
            self.globals.state = state_start.StartState(self.globals)
        if key == ord('z'):
            if len(self.current_nodes) != 0:
                self.globals.graph.nodes.remove(self.current_nodes.pop())

    def overlay_event(self):
        # self.globals.overlay.writeLine(2, "Node Id: %s, Node Type; " % (self.node.id))
        self.globals.overlay.writeLine(0, 'Press: "ENTER" to exit Mode, "c" for connect')
