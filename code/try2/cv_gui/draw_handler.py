import copy
import numpy as np
import threading

import cv2

from objects import *
from overlay import Overlay
from tools import Rate
from tools import cv_ext


class DrawHandler(threading.Thread):
    def __init__(self, handler):
        threading.Thread.__init__(self)

        self.max_rate = 30
        self.rate = Rate(self.max_rate)
        self.cursor_pos = (0, 0)
        self.image = cv2.imread('test.png')
        self.width = self.image.shape[1]
        self.height = self.image.shape[0]
        self.screen = None
        self.overlay = Overlay()

        self.name = "Roundabout Map"
        cv2.namedWindow(self.name)
        cv2.setMouseCallback(self.name, self.mouse_event)

        self.event = 60

        self.handler = handler
        handler.overlay=self.overlay

    def mouse_event(self, event, x, y, flags, param):
        self.event = 60
        self.cursor_pos = (x, y)
        self.handler.mouse_event(event, x, y)

    def run(self):
        while True:
            key = cv2.waitKey(1) & 0xFF
            if key == 27:
                self.handler.shutdown()
                self.shutdown()
                break
            self.handler.keyboard_event(key)
            self.handler.mode_event()

            if self.handler.update():
                self.screen = copy.copy(self.image)
                for node in self.handler.graph.nodes:
                    cv2.circle(self.screen, (node.pos[0], node.pos[1]), 2, (0, 0, 255), 2)
                    for lane in node.lanes:
                        cv_ext.draw_arrowed_polyline(self.screen, lane.points, (0, 255, 255))

                for lane in self.handler.graph.lanes:
                    cv2.polylines(self.screen, [np.array(lane.polygon)], False, (0, 255, 255))

                if self.handler.mark is not None:
                    cv2.circle(self.screen, self.handler.mark, 5, (0, 0, 255), 1)

                if self.handler.snapy is not None:
                    cv2.circle(self.screen, self.handler.snapy, 5, (0, 0, 0), 1)

            vis = copy.copy(self.screen)
            self.overlay.setCursor(self.cursor_pos)
            self.overlay.draw(vis)
            self.overlay.clear()
            if self.event > 1:
                self.event -= 1

            cv2.imshow(self.name, vis)
            self.rate.sleep_rate(self.event)

    def shutdown(self):
        cv2.destroyAllWindows()
