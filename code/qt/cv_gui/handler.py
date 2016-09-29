import copy
import numpy as np
import threading

import cv2

from objects import *
from overlay import Overlay
from parser import JsonHandler
from tools import Rate
from tools import cv_ext


class Handler(threading.Thread):
    def __init__(self, res, file):
        threading.Thread.__init__(self)
        np.set_printoptions(precision=4)
        self.max_rate = 5
        self.rate = Rate(self.max_rate)
        self.cursor_pos = (0, 0)
        img = cv2.imread('test.png')
        self.width = img.shape[1]  # res[0]
        self.height = img.shape[0]  # res[1]
        self.screen = img  # np.zeros((self.height, self.width, 3), np.uint8)
        self.overlay = Overlay()
        self.mode = 0
        self.step = 0
        self.parser = JsonHandler()
        self.graph = Graph()
        cv2.namedWindow("image")
        cv2.setMouseCallback("image", self.click_and_crop)
        self.texte = ["'ENTER': print graph to terminal, 's': save, 'l': load "]
        self.file = open(file, 'r+')
        self.event = 60
        self.mark = None
        self.elem = None
        self.snapy = None

    def click_and_crop(self, event, x, y, flags, param):
        self.event = 60
        self.cursor_pos = (x, y)
        snapy_node = self.graph.getNodeAt(x, y)
        try:
            self.snapy = snapy_node.pos
        except:
            self.snapy = None

        if event == cv2.EVENT_LBUTTONUP:
            if self.mode == 1:
                node = Node((x, y))
                # if len(self.graph.nodes) > 0:
                #    lane = Lane()
                #    self.graph.addLane(lane)
                #    lane.points.append(self.graph.nodes[-1].pos)
                #    lane.points.append(node.pos)
                #    self.graph.nodes[-1].connect(node, lane)
                self.graph.addNode(node)
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

    def run(self):
        while True:
            vis = copy.copy(self.screen)
            self.overlay.setCursor(self.cursor_pos)
            key = cv2.waitKey(1) & 0xFF

            if key == 27:
                self.shutdown()
                break
            elif key == ord('s'):
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

            self.overlay.writeLine(0, self.texte[0])
            self.overlay.writeLine(1, "mode: " + str(self.mode) + " step: " + str(self.step))

            for node in self.graph.nodes:
                cv2.circle(vis, (node.pos[0], node.pos[1]), 2, (0, 0, 255), 2)
                for lane in node.lanes:
                    cv_ext.draw_arrowed_polyline(vis, lane.points, (0, 255, 255))

            for lane in self.graph.lanes:
                cv2.polylines(vis, [np.array(lane.polygon)], True, (0, 255, 255))

            if self.mark is not None:
                cv2.circle(vis, self.mark, 5, (0, 0, 255), 1)

            if self.snapy is not None:
                cv2.circle(vis, self.snapy, 5, (0, 0, 0), 1)


            self.overlay.draw(vis)
            self.overlay.clear()
            if self.event > 1:
                self.event -= 1
            cv2.imshow("image", vis)
            self.rate.sleep_rate(self.event)

    def shutdown(self):
        cv2.destroyAllWindows()
        self.file.close()
