import state_start
from state import State
from connect_line import ConnectNodesState
from define_surface import SurfaceDefinitionState


class NodeOptionsState(State):
    def __init__(self, globals, node):
        super(NodeOptionsState, self).__init__(globals)
        self.node = node
        globals.mark = node.pos

    def mouse_event(self, event, x, y):
        pass

    def keyboard_event(self, key):
        if key == 10:
            self.globals.state = state_start.StartState(self.globals)
        if key == ord('c'):
            self.globals.state = ConnectNodesState(self.globals,self.node)
        if key == ord('s'):
            self.globals.state = SurfaceDefinitionState(self.globals, self.node)


    def overlay_event(self):
        self.globals.overlay.writeLine(2, "Node Id: %s, Node Type; " % (self.node.id))
        self.globals.overlay.writeLine(0, 'Press: "ENTER" to exit Mode, "c" for connect')
