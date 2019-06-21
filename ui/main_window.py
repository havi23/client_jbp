# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(261, 359)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 3, 261, 461))
        self.label.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("ui/img/noclass.png"))
        self.label.setObjectName("label")
        self.settings = QtWidgets.QPushButton(Dialog)
        self.settings.setGeometry(QtCore.QRect(50, 123, 161, 23))
        self.settings.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("ui/img/sett.bmp"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.settings.setIcon(icon)
        self.settings.setIconSize(QtCore.QSize(200, 150))
        self.settings.setObjectName("settings")
        self.binds = QtWidgets.QPushButton(Dialog)
        self.binds.setGeometry(QtCore.QRect(137, 164, 71, 23))
        self.binds.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("ui/img/binds.bmp"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.binds.setIcon(icon1)
        self.binds.setIconSize(QtCore.QSize(200, 150))
        self.binds.setObjectName("binds")
        self.change_class = QtWidgets.QPushButton(Dialog)
        self.change_class.setGeometry(QtCore.QRect(50, 163, 71, 23))
        self.change_class.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("ui/img/class.bmp"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.change_class.setIcon(icon2)
        self.change_class.setIconSize(QtCore.QSize(200, 150))
        self.change_class.setObjectName("change_class")
        self.start = QtWidgets.QPushButton(Dialog)
        self.start.setGeometry(QtCore.QRect(50, 299, 151, 31))
        self.start.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("ui/img/start.bmp"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.start.setIcon(icon3)
        self.start.setIconSize(QtCore.QSize(200, 150))
        self.start.setObjectName("start")
        self.info = QtWidgets.QPushButton(Dialog)
        self.info.setGeometry(QtCore.QRect(208, 71, 21, 20))
        self.info.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("ui/img/info.bmp"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.info.setIcon(icon4)
        self.info.setIconSize(QtCore.QSize(200, 150))
        self.info.setObjectName("info")
        self.close = QtWidgets.QPushButton(Dialog)
        self.close.setGeometry(QtCore.QRect(220, 30, 21, 20))
        self.close.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("ui/img/close.bmp"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.close.setIcon(icon5)
        self.close.setIconSize(QtCore.QSize(200, 150))
        self.close.setObjectName("close")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(80, 240, 141, 31))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("ui/img/hider.png"))
        self.label_2.setObjectName("label_2")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))


