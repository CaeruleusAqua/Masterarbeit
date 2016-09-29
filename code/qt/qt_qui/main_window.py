#!/usr/bin/env python
from PyQt4 import QtCore, QtGui

from qt_qui.drawing_area import DrawingArea


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.scaleFactor = 0.0

        self.imageLabel = DrawingArea()
        self.imageLabel.setBackgroundRole(QtGui.QPalette.Base)
        self.imageLabel.setSizePolicy(QtGui.QSizePolicy.Ignored,
                                      QtGui.QSizePolicy.Ignored)
        self.imageLabel.setScaledContents(True)

        self.scrollArea = QtGui.QScrollArea()
        self.scrollArea.setBackgroundRole(QtGui.QPalette.Dark)
        self.scrollArea.setWidget(self.imageLabel)
        self.scrollArea.setMouseTracking(True)

        self.setCentralWidget(self.scrollArea)

        self.createActions()
        self.createMenus()

        self.setWindowTitle("Image Viewer")
        self.resize(500, 400)

    def open(self):
        fileName = QtGui.QFileDialog.getOpenFileName(self, "Open File",
                                                     QtCore.QDir.currentPath())
        if fileName:
            image = QtGui.QImage(fileName)
            if image.isNull():
                QtGui.QMessageBox.information(self, "Image Viewer",
                                              "Cannot load %s." % fileName)
                return

            self.imageLabel.setPixmap(QtGui.QPixmap.fromImage(image))
            self.scaleFactor = 1.0

            self.fitToWindowAct.setEnabled(True)
            self.updateActions()

            if not self.fitToWindowAct.isChecked():
                self.imageLabel.adjustSize()

    def zoomIn(self):
        self.scaleImage(1.25)

    def zoomOut(self):
        self.scaleImage(0.8)

    def normalSize(self):
        self.imageLabel.adjustSize()
        self.scaleFactor = 1.0

    def fitToWindow(self):
        fitToWindow = self.fitToWindowAct.isChecked()
        self.scrollArea.setWidgetResizable(fitToWindow)
        if not fitToWindow:
            self.normalSize()

        self.updateActions()

    def createActions(self):
        self.openAct = QtGui.QAction("&Open...", self, shortcut="Ctrl+O",
                                     triggered=self.open)

        self.exitAct = QtGui.QAction("E&xit", self, shortcut="Ctrl+Q",
                                     triggered=self.close)

        self.zoomInAct = QtGui.QAction("Zoom &In (25%)", self,
                                       shortcut="Ctrl++", enabled=False, triggered=self.zoomIn)

        self.zoomOutAct = QtGui.QAction("Zoom &Out (25%)", self,
                                        shortcut="Ctrl+-", enabled=False, triggered=self.zoomOut)

        self.normalSizeAct = QtGui.QAction("&Normal Size", self,
                                           shortcut="Ctrl+S", enabled=False, triggered=self.normalSize)

        self.fitToWindowAct = QtGui.QAction("&Fit to Window", self,
                                            enabled=False, checkable=True, shortcut="Ctrl+F",
                                            triggered=self.fitToWindow)

    def createMenus(self):
        self.fileMenu = QtGui.QMenu("&File", self)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)

        self.viewMenu = QtGui.QMenu("&View", self)
        self.viewMenu.addAction(self.zoomInAct)
        self.viewMenu.addAction(self.zoomOutAct)
        self.viewMenu.addAction(self.normalSizeAct)
        self.viewMenu.addSeparator()
        self.viewMenu.addAction(self.fitToWindowAct)

        self.menuBar().addMenu(self.fileMenu)
        self.menuBar().addMenu(self.viewMenu)

    def updateActions(self):
        self.zoomInAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.zoomOutAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.normalSizeAct.setEnabled(not self.fitToWindowAct.isChecked())

    def scaleImage(self, factor):
        self.scaleFactor *= factor
        self.imageLabel.resize(self.scaleFactor * self.imageLabel.pixmap().size())

        self.adjustScrollBar(self.scrollArea.horizontalScrollBar(), factor)
        self.adjustScrollBar(self.scrollArea.verticalScrollBar(), factor)

        self.zoomInAct.setEnabled(self.scaleFactor < 3.0)
        self.zoomOutAct.setEnabled(self.scaleFactor > 0.333)

    def adjustScrollBar(self, scrollBar, factor):
        scrollBar.setValue(int(factor * scrollBar.value()
                               + ((factor - 1) * scrollBar.pageStep() / 2)))



