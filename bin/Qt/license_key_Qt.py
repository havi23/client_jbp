# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'license_key.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from bin.resource_to_exe import resource_path

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(301, 160)
        self.bg = QtWidgets.QLabel(Dialog)
        self.bg.setGeometry(QtCore.QRect(10, 10, 291, 141))
        self.bg.setText("")
        self.bg.setPixmap(QtGui.QPixmap(resource_path("bin\\img\\license\\license_key.png")))
        self.bg.setObjectName("bg")
        self.key_edit = QtWidgets.QLineEdit(Dialog)
        self.key_edit.setGeometry(QtCore.QRect(24, 86, 188, 20))
        self.key_edit.setObjectName("key_edit")
        self.description = QtWidgets.QLabel(Dialog)
        self.description.setGeometry(QtCore.QRect(80, 65, 146, 16))
        font = QtGui.QFont()
        font.setFamily("Futura-Normal")
        font.setPointSize(12)
        self.description.setFont(font)
        self.description.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.description.setStyleSheet("color: silver")
        self.description.setAlignment(QtCore.Qt.AlignCenter)
        self.description.setObjectName("description")
        self.submit = QtWidgets.QLabel(Dialog)
        self.submit.setGeometry(QtCore.QRect(222, 88, 61, 16))
        self.submit.setText("")
        self.submit.setObjectName("submit")
        self.website = QtWidgets.QLabel(Dialog)
        self.website.setGeometry(QtCore.QRect(76, 118, 149, 18))
        self.website.setText("")
        self.website.setObjectName("website")
        self.error = QtWidgets.QLabel(Dialog)
        self.error.setGeometry(QtCore.QRect(177, 118, 101, 16))
        font = QtGui.QFont()
        font.setFamily("Futura-Normal")
        font.setPointSize(12)
        self.error.setFont(font)
        self.error.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.error.setStyleSheet("color: red")
        self.error.setAlignment(QtCore.Qt.AlignCenter)
        self.error.setObjectName("error")
        self.exit_ = QtWidgets.QLabel(Dialog)
        self.exit_.setGeometry(QtCore.QRect(250, 17, 38, 17))
        self.exit_.setText("")
        self.exit_.setObjectName("exit_")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.description.setText(_translate("Dialog", "Enter a license key"))
        self.error.setText(_translate("Dialog", "wrong key"))

