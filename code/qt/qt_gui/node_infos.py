from PyQt4.QtCore import *
from PyQt4.QtGui import *


class MyTable(QTableWidget):
    def __init__(self):
        QTableWidget.__init__(self)
        self.data = {'col1': ['1', '2', '3'], 'col2': ['4', '5', '6'], 'col3': ['7', '8', '9']}
        self.setmydata()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()

    def setmydata(self):

        horHeaders = []
        for n, key in enumerate(sorted(self.data.keys())):
            horHeaders.append(key)
            for m, item in enumerate(self.data[key]):
                newitem = QTableWidgetItem(item)
                self.setItem(m, n, newitem)
        self.setHorizontalHeaderLabels(horHeaders)
