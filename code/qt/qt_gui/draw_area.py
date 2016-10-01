from PyQt4.QtCore import *
from PyQt4.QtGui import *

from mouse_event import MouseEvent


class DrawArea(QWidget):
    def __init__(self, handler):
        QGraphicsView.__init__(self)

        self.handler = handler
        self.setMouseTracking(True)
        self.rightPressed = False
        self.image = None

    def setPixmap(self, image):
        self.image = image
        self.setFixedSize(image.size())

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.NoButton:
            self.handler.mouse_event(MouseEvent.EVENT_MOVE, event.pos().x(), event.pos().y())
        self.update()

    def mouseReleaseEvent(self, event):
        if self.rightPressed:
            self.rightPressed = False
            self.handler.mouse_event(MouseEvent.EVENT_RBUTTONUP, event.pos().x(), event.pos().y())
        else:
            self.handler.mouse_event(MouseEvent.EVENT_LBUTTONUP, event.pos().x(), event.pos().y())
        self.update()

    def mousePressEvent(self, event):
        self._start = event.pos()
        if event.buttons() == Qt.LeftButton:
            self.handler.mouse_event(MouseEvent.EVENT_LBUTTONDOWN, event.pos().x(), event.pos().y())
        elif event.buttons() == Qt.RightButton:
            self.rightPressed = True
            self.handler.mouse_event(MouseEvent.EVENT_RBUTTONDOWN, event.pos().x(), event.pos().y())
        self.update()

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.drawPixmap(QPoint(0, 0), self.image)
        # painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(Qt.red, 2, Qt.SolidLine)
        painter.setPen(pen)
        for node in self.handler.graph.nodes:
            # painter.drawPoint(node.pos[0], node.pos[1])
            painter.setBrush(Qt.red)
            painter.drawEllipse(QPoint(node.pos[0], node.pos[1]), 3, 3)
            for lane in node.lanes:
                pass
                # cv_ext.draw_arrowed_polyline(self.screen, lane.points, (0, 255, 255))

            for lane in self.handler.graph.lanes:
                pass
                # cv2.polylines(self.screen, [np.array(lane.polygon)], False, (0, 255, 255))

        if self.handler.mark is not None:
            pass
            # cv2.circle(self.screen, self.handler.mark, 5, (0, 0, 255), 1)

        if self.handler.snapy is not None:
            pen = QPen(Qt.black, 2, Qt.SolidLine)
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)
            painter.drawEllipse(QPoint(self.handler.snapy[0], self.handler.snapy[1]), 4, 4)
            # cv2.circle(self.screen, self.handler.snapy, 5, (0, 0, 0), 1)

        painter.end()

    def sizeHint(self):
        return QSize(500, 500)
