# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'control_center.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1050, 880)
        self.label_map = QtWidgets.QLabel(Form)
        self.label_map.setGeometry(QtCore.QRect(10, 10, 1031, 861))
        self.label_map.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.label_map.setText("")
        self.label_map.setObjectName("label_map")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))


