#!/usr/bin/env python2
from PyQt4 import QtCore, QtGui
from qt_gui import MainWindow
from qt_gui import MouseEvent



if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)
    imageViewer = MainWindow()
    imageViewer.show()
    sys.exit(app.exec_())