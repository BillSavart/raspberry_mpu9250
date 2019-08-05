# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'draw.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(951, 753)
        self.AddPicBtn = QtWidgets.QPushButton(Form)
        self.AddPicBtn.setGeometry(QtCore.QRect(30, 690, 121, 51))
        self.AddPicBtn.setObjectName("AddPicBtn")
        self.OkBtn = QtWidgets.QPushButton(Form)
        self.OkBtn.setGeometry(QtCore.QRect(780, 690, 121, 51))
        self.OkBtn.setObjectName("OkBtn")
        self.PicLabel = QtWidgets.QLabel(Form)
        self.PicLabel.setGeometry(QtCore.QRect(20, 10, 911, 641))
        self.PicLabel.setText("")
        self.PicLabel.setObjectName("PicLabel")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.AddPicBtn.setText(_translate("Form", "Add Picture"))
        self.OkBtn.setText(_translate("Form", "OK"))


