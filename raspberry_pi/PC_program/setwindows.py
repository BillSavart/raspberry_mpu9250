from windows import Ui_Form
import numpy as np
import os
import sys
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtGui import *
from PyQt5.QtCore import QTimer, Qt
import cv2
import time
import global_data

class AppWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.initVar()
        self.img_map_loading()
        self.timer=QTimer(self)
        self.timer.timeout.connect(self.update_image)
        self.timer.start(500)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.btn_info.clicked.connect(self.on_click_btn_info)
        self.ui.btn_map.clicked.connect(self.on_click_btn_map)
        self.ui.btn_image.clicked.connect(self.on_click_btn_image)
        self.ui.btn_choose.setEnabled(False)
        self.ui.btn_ok.setEnabled(False)     
        self.show()

    def initVar(self):
        self.image_image = np.zeros((800,800,3),np.uint8)
        self.image_map = np.zeros((800,800,3),np.uint8)
        self.image_info = np.zeros((800,800,3),np.uint8)
        self.keep = np.zeros((800,800,3),np.uint8)
        self.img_fireman = [ ]
        self.image_image_flag = False
        self.image_map_flag = True
        self.image_info_flag = False   
        self.middle_x = 1170
        self.middle_y = 700
 
    def on_click_btn_info(self):
        self.image_image_flag = False
        self.image_map_flag = False
        self.image_info_flag = True
        self.ui.btn_choose.setEnabled(False)
        self.ui.btn_ok.setEnabled(False)

    def on_click_btn_map(self):
        self.image_image_flag = False
        self.image_map_flag = True
        self.image_info_flag = False
        self.ui.btn_choose.setEnabled(True)
        self.ui.btn_ok.setEnabled(True)

    def on_click_btn_image(self):
        self.image_image_flag = True
        self.image_map_flag = False
        self.image_info_flag = False
        self.ui.btn_choose.setEnabled(False)
        self.ui.btn_ok.setEnabled(False)     

    def update_image(self):
        image = self.image_map
        if(self.image_image_flag):
            image = self.image_image
        elif(self.image_map_flag):
            image = self.image_map
        elif(self.image_info_flag):
            image = self.image_info
        else:
            pass

#        cv2.imshow("Image",image)
#        cv2.waitKey(0)
        QIm = QImage(image.data, image.shape[1], image.shape[0],image.shape[1] *image.shape[2],QImage.Format_RGB888)
        self.ui.label.setPixmap(QPixmap.fromImage(QIm))

    def mousePressEvent(self,event):
        if(event.buttons() == Qt.LeftButton):
            print("Left Mouse, x: ",event.pos().x())
            print("Left Mouse, y: ",event.pos().y())

    def mouseReleaseEvent(self,event):
        if(event.buttons() == Qt.LeftButton):
            print("Left Mouse, x: ",event.pos().x())
            print("Left Mouse, y: ",event.pos().y())

    def img_map_loading(self):
        fireman_img_map_path = "../IMAGE/fireman.png"
        map_img_map_path = "../IMAGE/1f.png"
        if(os.path.isfile(fireman_img_map_path)):
            print("Reading FireFighter Image...")
            while(len(self.img_fireman) == 0):
                self.img_fireman = cv2.imread(fireman_img_map_path)
            self.img_fireman = cv2.resize(self.img_fireman,(50,50))
        else:
            print("There is no FireFighter Image")

        img_map = [] 
        print("Reading Environment Map...")
        if(os.path.isfile(map_img_map_path)):
            while(len(img_map) == 0):
                img_map = cv2.imread(map_img_map_path)
        print("Merge Map For Four FireFighters...")
        img_map = np.hstack((img_map,img_map))
        img_map = np.vstack((img_map,img_map))
 
        print("Drawing Security Line...")
        img_map = cv2.line(img_map,(5,5),(self.middle_x*2,5),(0,139,0),10,6)
        img_map = cv2.line(img_map,(5,self.middle_y),(self.middle_x*2,self.middle_y),(0,139,0),10,6)
        img_map = cv2.line(img_map,(5,self.middle_y*2),(self.middle_x*2,self.middle_y*2),(0,139,0),10,6)
        img_map = cv2.line(img_map,(5,5),(5,self.middle_y*2),(0,139,0),10,6)
        img_map = cv2.line(img_map,(self.middle_x,5),(self.middle_x,self.middle_y*2),(0,139,0),10,6)
        img_map = cv2.line(img_map,(self.middle_x*2,5),(self.middle_x*2,self.middle_y*2),(0,139,0),10,6)
 
        print("Set Initialize Map")
        self.keep = img_map.copy()
        self.image_map = img_map.copy()

image_image = cv2.imread('../IMAGE/1f.png')
image_map = cv2.imread('../IMAGE/5f.png') 
image_info = cv2.imread('../IMAGE/fireman.png') 

app = QApplication(sys.argv)
w = AppWindow()
w.show()
sys.exit(app.exec_())
