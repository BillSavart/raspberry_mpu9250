# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'setMap.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1006, 841)
        self.graphicsView = QtWidgets.QGraphicsView(Form)
        self.graphicsView.setGeometry(QtCore.QRect(10, 10, 991, 751))
        self.graphicsView.setObjectName("graphicsView")
        self.btnLoadMap = QtWidgets.QPushButton(Form)
        self.btnLoadMap.setGeometry(QtCore.QRect(10, 770, 131, 61))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setItalic(True)
        self.btnLoadMap.setFont(font)
        self.btnLoadMap.setObjectName("btnLoadMap")
        self.btnMapInit = QtWidgets.QPushButton(Form)
        self.btnMapInit.setGeometry(QtCore.QRect(160, 770, 131, 61))
        font = QtGui.QFont()
        font.setPointSize(36)
        font.setItalic(True)
        self.btnMapInit.setFont(font)
        self.btnMapInit.setObjectName("btnMapInit")
        self.btnOk = QtWidgets.QPushButton(Form)
        self.btnOk.setGeometry(QtCore.QRect(860, 770, 141, 61))
        font = QtGui.QFont()
        font.setPointSize(36)
        font.setItalic(True)
        self.btnOk.setFont(font)
        self.btnOk.setObjectName("btnOk")
        self.labelNote = QtWidgets.QLabel(Form)
        self.labelNote.setGeometry(QtCore.QRect(310, 770, 531, 61))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setItalic(True)
        self.labelNote.setFont(font)
        self.labelNote.setText("")
        self.labelNote.setObjectName("labelNote")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.btnLoadMap.setText(_translate("Form", "LOAD MAP"))
        self.btnMapInit.setText(_translate("Form", "Start"))
        self.btnOk.setText(_translate("Form", "OK"))


