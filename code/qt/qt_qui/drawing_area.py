from PyQt4 import QtCore,QtGui


class DrawingArea(QtGui.QLabel):
    def __init__(self):
        super(DrawingArea, self).__init__()
        self.setMouseTracking(True)

    def mouseMoveEvent(self, event):
        print event.pos()
        if event.buttons() == QtCore.Qt.NoButton:
            print "Simple mouse motion"
        elif event.buttons() == QtCore.Qt.LeftButton:
            print "Left click drag"
            qp = QtGui.QPainter()
            qp.begin(self)
            self.drawBrushes(qp)
            qp.end()
        elif event.buttons() == QtCore.Qt.RightButton:
            print "Right click drag"


    def drawBrushes(self, qp):
        brush = QtGui.QBrush(QtCore.Qt.SolidPattern)
        qp.setBrush(brush)
        qp.drawRect(10, 15, 90, 60)

        brush.setStyle(QtCore.Qt.Dense1Pattern)
        qp.setBrush(brush)
        qp.drawRect(130, 15, 90, 60)

        brush.setStyle(QtCore.Qt.Dense2Pattern)
        qp.setBrush(brush)
        qp.drawRect(250, 15, 90, 60)

        brush.setStyle(QtCore.Qt.Dense3Pattern)
        qp.setBrush(brush)
        qp.drawRect(10, 105, 90, 60)

        brush.setStyle(QtCore.Qt.DiagCrossPattern)
        qp.setBrush(brush)
        qp.drawRect(10, 105, 90, 60)

        brush.setStyle(QtCore.Qt.Dense5Pattern)
        qp.setBrush(brush)
        qp.drawRect(130, 105, 90, 60)

        brush.setStyle(QtCore.Qt.Dense6Pattern)
        qp.setBrush(brush)
        qp.drawRect(250, 105, 90, 60)

        brush.setStyle(QtCore.Qt.HorPattern)
        qp.setBrush(brush)
        qp.drawRect(10, 195, 90, 60)

        brush.setStyle(QtCore.Qt.VerPattern)
        qp.setBrush(brush)
        qp.drawRect(130, 195, 90, 60)

        brush.setStyle(QtCore.Qt.BDiagPattern)
        qp.setBrush(brush)
        qp.drawRect(250, 195, 90, 60)
