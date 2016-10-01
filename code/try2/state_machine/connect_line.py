import cv2

import state_start
from objects import *
from state import State
import node_options


class ConnectNodesState(State):
    def __init__(self, globals, node):
        super(ConnectNodesState, self).__init__(globals)
        self.connected = False
        self.lane = None
        self.node = node
        self.connectedNode = None

    def mouse_event(self, event, x, y):
        self.enableHover(self.globals.graph.getNodeAt(x, y))

        if event == cv2.EVENT_LBUTTONDOWN and not self.connected and self.snapy_node and self.snapy_node is not self.node:
            self.lane = Lane()
            self.lane.points.append(self.node.pos)
            self.node.connect(self.snapy_node, self.lane)
            self.connected = True
            self.connectedNode = self.snapy_node
        elif event == cv2.EVENT_LBUTTONDOWN and self.connected and self.snapy_node != self.connectedNode:
            self.lane.points.append((x,y))

        elif event == cv2.EVENT_LBUTTONDOWN and self.connected and self.snapy_node == self.connectedNode:
            self.lane.points.append(self.snapy_node.pos)
            self.globals.state = node_options.NodeOptionsState(self.globals, self.node)

    def keyboard_event(self, key):
        if key == 10:
            self.globals.state = state_start.StartState(self.globals)
        if key == ord('z'):
            self.globals.graph.popLastNode()

    def overlay_event(self):
        if self.snapy_node:
            self.globals.overlay.writeLine(2, "Node Id: %s, Node Type; " % (self.snapy_node.id))

        self.globals.overlay.writeLine(0, 'Press: "ENTER" to exit Mode')
