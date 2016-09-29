import cv2

from objects import *
from parser import JsonHandler
from state_start import StartState


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
        self.snapy_node = None
        self.updated = True
        self.overlay = None
        self.cursor_pos = None

        self.modeObj = StartState(self)

    def update(self):
        tmp = self.updated
        self.updated = False
        return tmp

    def mouse_event(self, event, x, y):

        self.cursor_pos = (x, y)
        snapy_node = self.graph.getNodeAt(x, y)
        self.snapy_node = snapy_node
        try:
            self.snapy = snapy_node.pos
        except:
            self.snapy = None

        if event == cv2.EVENT_LBUTTONDOWN:
            if self.mode == 1:
                self.graph.addNode(Node((x, y)))
                self.mode = 0

            elif self.mode == 2:
                if self.step == 0:
                    self.elem['firstNode'] = snapy_node
                    if self.elem['firstNode']:
                        self.mark = snapy_node.pos
                        lane = Lane()
                        self.elem['lane'] = lane
                        self.graph.addLane(lane)
                        snapy_node.lanes.append(lane)
                        lane.anchor = snapy_node
                        lane.points.append(snapy_node.pos)
                        self.step = 1

                elif self.step == 1:
                    lane = self.elem['lane']
                    if snapy_node:
                        lane.points.append(snapy_node.pos)
                        lane.nodes.append(snapy_node)
                        self.mode = 0
                        self.step = 0
                        self.elem = None
                    else:
                        lane.points.append((x, y))
            elif self.mode == 3:
                if self.step == 0:
                    self.elem['firstNode'] = snapy_node
                    if self.elem['firstNode']:
                        self.mark = self.elem['firstNode'].pos
                        self.step = 1
                elif self.step == 1:
                    self.elem['secondNode'] = snapy_node
                    if self.elem['secondNode']:
                        self.mark = self.elem['secondNode'].pos
                        for lane in self.elem['firstNode'].lanes:
                            if snapy_node in lane.nodes:
                                self.elem['lane'] = lane
                                lane.polygon.append(lane.anchor.pos)
                                self.step = 2
                                break
                elif self.step == 2:
                    if snapy_node == self.elem['firstNode']:
                        self.step = 0
                        self.mode = 0
                    else:
                        self.elem['lane'].polygon.append((x, y))

    def keyboard_event(self, key):
        if key == ord('s'):
            self.file.seek(0)
            self.file.truncate()
            self.file.write(self.parser.serialize(self.graph))
            self.overlay.timedMessage("saved..", 1)

        elif key == ord('l'):
            self.file.seek(0)
            self.graph = self.parser.deserialize(self.file.read())
            self.overlay.timedMessage("loaded..", 1)

        elif key == ord('n'):
            self.mode = 1

        elif key == ord('a'):
            self.elem = dict()
            self.mode = 3
            self.step = 0

        elif key == ord('c'):
            self.elem = dict()
            self.mode = 2
            self.step = 0

        if self.mode == 2:
            if self.step == 1:
                self.mark = self.elem['firstNode'].pos
                if key == ord('z'):
                    lane = self.elem['lane']
                    try:
                        lane.points.pop()
                    except:
                        pass
        self.updated = True

    def mode_event(self):
        if self.snapy_node:
            self.overlay.writeLine(2, "Node Id: %s, Node Type; " % (self.snapy_node.id))
        if self.mode == 0:
            self.overlay.writeLine(0, "Key's: 's': save, 'l': load    click on Node for more options")
        elif self.mode == 1:
            self.overlay.writeLine(0, "Key's: 'c': connect ")

        self.overlay.writeLine(1, "Mode: %i , Step: %i " % (self.mode, self.step))

    def shutdown(self):
        self.file.close()
