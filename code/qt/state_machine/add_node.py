from qt_gui.mouse_event import MouseEvent

import start
from objects import *
from state import State


class AddNodeState(State):
    def __init__(self, globals):
        super(AddNodeState, self).__init__(globals)

    def mouse_event(self, event, x, y):
        self.enableHover(self.globals.graph.getNodeAt(x, y))
        if event == MouseEvent.EVENT_LBUTTONDOWN:
            self.globals.graph.addNode(Node((x, y)))

    def keyboard_event(self, key):
        if key == 10:
            self.globals.state = start.StartState(self.globals)
        if key == ord('z'):
            self.globals.graph.popLastNode()

    def overlay_event(self):
        if self.snapy_node:
            self.globals.overlay.writeLine(2, "Node Id: %s, Node Type; " % self.snapy_node.id)

        self.globals.overlay.writeLine(0, 'Press "ENTER" to exit Mode')
