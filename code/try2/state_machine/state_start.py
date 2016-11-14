import cv2

from add_node import AddNodeState
from define_surface import SurfaceDefinitionState
from node_options import NodeOptionsState
from state import State


class StartState(State):
    def __init__(self, globals):
        super(StartState, self).__init__(globals)
        self.drag = None

    def mouse_event(self, event, x, y):
        self.enableHover(self.globals.graph.getNodeAt(x, y))
        bord = self.globals.graph.getBorderAt(x, y)
        # if bord:
        #    print "!!!"
        if event == cv2.EVENT_LBUTTONDOWN and self.snapy_node and self.snapy_node.movable:
            self.snapy_node.setPos((x, y))
            self.drag = self.snapy_node

        elif event == cv2.EVENT_LBUTTONDBLCLK and self.snapy_node:
            self.globals.state = NodeOptionsState(self.globals, self.snapy_node)

        elif event == cv2.EVENT_LBUTTONUP and self.drag:
            self.drag.setPos((x, y))
            self.drag = None

        elif self.drag:
            self.drag.setPos((x, y))

    def keyboard_event(self, key):
        if key == ord('n'):
            self.globals.state = AddNodeState(self.globals)
        if key == ord('s'):
            self.globals.state = SurfaceDefinitionState(self.globals)

    def overlay_event(self):
        if self.snapy_node:
            self.globals.overlay.writeLine(2, "Node Id: %s, Node Type; " % (self.snapy_node.id))

        self.globals.overlay.writeLine(0, "Key's: 's': save, 'l': load    click on Node for more options")
