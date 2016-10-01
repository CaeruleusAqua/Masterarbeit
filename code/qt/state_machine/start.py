
from state import State
from add_node import AddNodeState
from connect_line import ConnectNodesState
from qt_gui.mouse_event import MouseEvent


class StartState(State):
    def __init__(self, globals):
        super(StartState, self).__init__(globals)
        self.drag = None

    def mouse_event(self, event, x, y):
        self.enableHover(self.globals.graph.getNodeAt(x, y))
        if event == MouseEvent.EVENT_LBUTTONDOWN and self.snapy_node:
            self.snapy_node.pos = (x, y)
            self.drag = self.snapy_node

        elif event == MouseEvent.EVENT_LBUTTONDBLCLK and self.snapy_node:
            self.globals.state = ConnectNodesState(self.globals)

        elif event == MouseEvent.EVENT_LBUTTONUP and self.drag:
            self.drag.pos = (x, y)
            self.drag = None

        elif self.drag:
            self.drag.pos = (x, y)

    def keyboard_event(self, key):
        if key == ord('n'):
            self.globals.state = AddNodeState(self.globals)

    def overlay_event(self):
        if self.snapy_node:
            self.globals.overlay.writeLine(2, "Node Id: %s, Node Type; " % (self.snapy_node.id))

        self.globals.overlay.writeLine(0, "Key's: 's': save, 'l': load    click on Node for more options")
