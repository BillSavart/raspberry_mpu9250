import sys
from mainUi import Ui_Form
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileSystemModel, QTreeView,QVBoxLayout
from PyQt5.QtGui import QImage,QPixmap,QCursor
import os
import cv2
import time

MAP_FILE_DIST = "../IMAGE/image_draw.JPG"

class MainWindow(QMainWindow, Ui_Form):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        img = cv2.imread(MAP_FILE_DIST,1)
        height, weight, channel = img.shape
        image = QImage(img.data,height,weight,3,QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(image)
        self.label_map.setPixmap(pixmap)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
