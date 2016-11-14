import copy
import numpy as np
import threading

import cv2

from overlay import Overlay
from state_machine import Scenario
from tools import Rate


class DrawHandler(threading.Thread):
    def __init__(self, handler):
        threading.Thread.__init__(self)

        self.max_rate = 60
        self.rate = Rate(self.max_rate)
        self.cursor_pos = (0, 0)
        # self.image = cv2.imread('test2.jpg')
        self.image = np.zeros((800, 800, 3))
        self.width = self.image.shape[1]
        self.height = self.image.shape[0]
        self.screen = None
        self.zero = (400, 400)
        self.meter2pix_scale = 5.0
        self.overlay = Overlay()

        self.name = "Roundabout Map"
        cv2.namedWindow(self.name)
        cv2.setMouseCallback(self.name, self.mouse_event)

        self.event = 200

        self.handler = handler
        self.scenario = Scenario(handler)
        handler.overlay = self.overlay

    def mouse_event(self, event, x, y, flags, param):
        self.event = 200
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
            self.handler.overlay_event()

            if self.handler.update():
                self.screen = copy.copy(self.image)
                for obj in self.handler.graph.drawables:
                    obj.draw(self.screen, self.meter2pix_scale, self.zero)

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
