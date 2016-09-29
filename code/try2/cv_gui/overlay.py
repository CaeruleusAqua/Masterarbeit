import time

import cv2


class Overlay:
    def __init__(self, lines=3, scale=1):
        self.font = cv2.FONT_HERSHEY_PLAIN
        self.scale = scale
        self.text_height = cv2.getTextSize("Test", self.font, self.scale, 1)[0][1]
        self.width = None
        self.height = None
        self.lines = []
        self.errors = []
        self.nr_lines = lines
        self.linespace = 0.7
        self.fps=50
        self.show_fps = True
        self.timestamp = time.time()
        self.cursor = None
        self.color = (255, 255, 0)
        self.tMessage = list()
        for x in xrange(lines):
            self.lines.append(("", self.color))

    def setFont(self, font=cv2.FONT_HERSHEY_PLAIN):
        self.font = font

    def addLine(self, text, color=(255, 255, 0)):
        self.lines.append((text, color))

    def writeLine(self, line, text):
        self.lines[line] = (text, self.color)

    def addError(self, text):
        self.errors.append(text)

    def setCursor(self, cursor):
        self.cursor = cursor

    def timedMessage(self, message, duration):
        print message
        self.tMessage.append([message, time.time() + duration])

    def draw(self, image):

        self.width = image.shape[1]
        self.height = image.shape[0]
        bar_height = int(self.text_height * self.linespace + (len(self.lines) + len(self.errors)) * self.text_height * (1 + self.linespace))
        overlay = image.copy()
        alpha = 0.4
        cv2.rectangle(overlay, (0, 0), (self.width, bar_height), (0, 0, 0), -1)
        cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0, image)
        for i, line in enumerate(self.lines):
            cv2.putText(image, line[0], (5, int((1 + i) * (self.text_height * (1 + self.linespace)))), self.font, self.scale, (255, 255, 0))

        for i, line in enumerate(self.errors):
            cv2.putText(image, line, (5, int((1 + i + len(self.lines)) * (self.text_height * (1 + self.linespace)))), self.font, self.scale, (0, 0, 255))

        for i, line in enumerate(self.tMessage):
            cv2.putText(image, line[0], (5, int((1 + i + len(self.errors) + len(self.lines)) * (self.text_height * (1 + self.linespace)))), self.font,
                        self.scale, (0, 0, 255))
            if line[1] < time.time():
                self.tMessage.remove(line)

        if self.cursor != None:
            cursor_text = "( " + str(self.cursor[0]) + " , " + str(self.cursor[1]) + " )"
            cwidth = cv2.getTextSize(cursor_text, self.font, self.scale, 1)[0][0]
            cv2.putText(image, cursor_text, (self.width - cwidth - 5, int(self.text_height * (1 + self.linespace))), self.font, self.scale, (255, 255, 0))

        if self.show_fps:
            stamp = time.time()
            self.fps = (1.0 / (stamp - self.timestamp))
            fps = str(round(self.fps,1)) + " fps"
            self.timestamp=stamp
            cwidth = cv2.getTextSize(fps, self.font, self.scale, 1)[0][0]
            cv2.putText(image, fps, (self.width - cwidth - 5, int(self.text_height *2* (1 + self.linespace))), self.font, self.scale, (255, 255, 0))

    def clear(self):
        self.lines = []
        self.cursor = None
        for x in xrange(self.nr_lines):
            self.lines.append(("", self.color))

    def clearErrors(self):
        self.errors = []
