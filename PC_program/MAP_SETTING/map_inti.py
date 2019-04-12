import sys
from setMapUi import Ui_Form
from PyQt5.QtWidgets import QMainWindow, QApplication
import os

MAP_FILE_DIST = "../../IMAGE/indoor_position.JPG"


class MainWindow(QMainWindow, Ui_Form):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.btnOk.clicked.connect(self.btnOk_onclick)
        self.btnLoadMap.clicked.connect(self.btnLoadMap_onclick)
        self.btnMapInit.clicked.connect(self.btnMapInit_onclick)

    def btnLoadMap_onclick(self):

    def btnMapInit_onclick(self): 

    def btnOk_onclick(self):


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
