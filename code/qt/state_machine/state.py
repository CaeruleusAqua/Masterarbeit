from abc import ABCMeta, abstractmethod
from PyQt4.QtGui import *

class State:
    __metaclass__ = ABCMeta

    def __init__(self, globals):
        self.globals = globals
        self.snapy_node = None

    def enableHover(self,node):
        self.snapy_node = node
        if self.snapy_node:
            self.globals.snapy = self.snapy_node.pos
            self.globals.info.setItem(0, 0, QTableWidgetItem("Node"))
            self.globals.info.setItem(0, 1, QTableWidgetItem(str(self.snapy_node.id)))
        else:
            self.globals.snapy = None


    @abstractmethod
    def mouse_event(self, event):
        pass

    @abstractmethod
    def keyboard_event(self, key):
        pass

    @abstractmethod
    def overlay_event(self):
        pass
