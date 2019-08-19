# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1074, 835)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(0, 0, 1071, 731))
        self.label.setText("")
        self.label.setObjectName("label")
        self.btn_image = QtWidgets.QPushButton(Form)
        self.btn_image.setGeometry(QtCore.QRect(20, 750, 121, 61))
        self.btn_image.setObjectName("btn_image")
        self.btn_map = QtWidgets.QPushButton(Form)
        self.btn_map.setGeometry(QtCore.QRect(180, 750, 121, 61))
        self.btn_map.setObjectName("btn_map")
        self.btn_info = QtWidgets.QPushButton(Form)
        self.btn_info.setGeometry(QtCore.QRect(340, 750, 121, 61))
        self.btn_info.setObjectName("btn_info")
        self.btn_choose = QtWidgets.QPushButton(Form)
        self.btn_choose.setGeometry(QtCore.QRect(770, 740, 121, 61))
        self.btn_choose.setObjectName("btn_choose")
        self.btn_ok = QtWidgets.QPushButton(Form)
        self.btn_ok.setGeometry(QtCore.QRect(910, 740, 121, 61))
        self.btn_ok.setObjectName("btn_ok")

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


