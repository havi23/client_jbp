# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'license_key.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(301, 160)
        self.bg = QtWidgets.QLabel(Dialog)
        self.bg.setGeometry(QtCore.QRect(10, 10, 291, 141))
        self.bg.setText("")
        self.bg.setPixmap(QtGui.QPixmap("bin/img/license/bg.png"))
        self.bg.setObjectName("bg")
        self.key_edit = QtWidgets.QLineEdit(Dialog)
        self.key_edit.setGeometry(QtCore.QRect(25, 63, 188, 20))
        self.key_edit.setObjectName("key_edit")
        self.submit = QtWidgets.QLabel(Dialog)
        self.submit.setGeometry(QtCore.QRect(218, 61, 62, 25))
        self.submit.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.submit.setText("")
        self.submit.setPixmap(QtGui.QPixmap("bin/img/license/submit.png"))
        self.submit.setObjectName("submit")
        self.website = QtWidgets.QLabel(Dialog)
        self.website.setGeometry(QtCore.QRect(229, 35, 63, 21))
        self.website.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.website.setText("")
        self.website.setPixmap(QtGui.QPixmap("bin/img/license/website.png"))
        self.website.setObjectName("website")
        self.error = QtWidgets.QLabel(Dialog)
        self.error.setGeometry(QtCore.QRect(23, 91, 257, 46))
        font = QtGui.QFont()
        font.setFamily("Futura-Normal")
        font.setPointSize(12)
        self.error.setFont(font)
        self.error.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.error.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.error.setStyleSheet("color: red")
        self.error.setScaledContents(False)
        self.error.setAlignment(QtCore.Qt.AlignCenter)
        self.error.setWordWrap(True)
        self.error.setObjectName("error")
        self.exit_ = QtWidgets.QLabel(Dialog)
        self.exit_.setGeometry(QtCore.QRect(250, 17, 38, 17))
        self.exit_.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.exit_.setText("")
        self.exit_.setObjectName("exit_")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.error.setText(_translate("Dialog", "wrong key"))

