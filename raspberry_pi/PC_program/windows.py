# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'setWindows.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1822, 976)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(0, 0, 1811, 901))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("Project/raspberry_mpu9250/raspberry_pi/IMAGE/1f.png"))
        self.label.setObjectName("label")
        self.btn_image = QtWidgets.QPushButton(Form)
        self.btn_image.setGeometry(QtCore.QRect(20, 920, 121, 61))
        self.btn_image.setObjectName("btn_image")
        self.btn_map = QtWidgets.QPushButton(Form)
        self.btn_map.setGeometry(QtCore.QRect(190, 920, 121, 61))
        self.btn_map.setObjectName("btn_map")
        self.btn_info = QtWidgets.QPushButton(Form)
        self.btn_info.setGeometry(QtCore.QRect(350, 920, 121, 61))
        self.btn_info.setObjectName("btn_info")
        self.btn_choose = QtWidgets.QPushButton(Form)
        self.btn_choose.setGeometry(QtCore.QRect(1400, 930, 85, 51))
        self.btn_choose.setObjectName("btn_choose")
        self.btn_ok = QtWidgets.QPushButton(Form)
        self.btn_ok.setGeometry(QtCore.QRect(1620, 930, 85, 51))
        self.btn_ok.setObjectName("btn_ok")
        self.btn_remove = QtWidgets.QPushButton(Form)
        self.btn_remove.setGeometry(QtCore.QRect(1510, 930, 85, 51))
        self.btn_remove.setObjectName("btn_remove")
        self.btn_reset = QtWidgets.QPushButton(Form)
        self.btn_reset.setGeometry(QtCore.QRect(1510, 930, 85, 51))
        self.btn_reset.setObjectName("btn_reset")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.btn_image.setText(_translate("Form", "Show Image"))
        self.btn_map.setText(_translate("Form", "Show Map"))
        self.btn_info.setText(_translate("Form", "Show Info"))
        self.btn_choose.setText(_translate("Form", "Choose"))
        self.btn_ok.setText(_translate("Form", "OK"))
        self.btn_remove.setText(_translate("Form", "Remove"))
        self.btn_reset.setText(_translate("Form", "Reset Time"))


