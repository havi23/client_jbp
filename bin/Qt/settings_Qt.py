# -*- coding: utf-8 -*-

# Form implementation generated from reading bin file 'settings.bin'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from bin.resource_to_exe import resource_path

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(497, 423)
        self.bg = QtWidgets.QLabel(Dialog)
        self.bg.setGeometry(QtCore.QRect(20, 20, 471, 401))
        self.bg.setText("")
        self.bg.setPixmap(QtGui.QPixmap(resource_path("bin/img/settings/settings.png")))
        self.bg.setObjectName("bg")
        self.cwp = QtWidgets.QPushButton(Dialog)
        self.cwp.setGeometry(QtCore.QRect(260, 218, 181, 31))
        self.cwp.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.cwp.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(resource_path("bin/img/settings/cwp.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cwp.setIcon(icon)
        self.cwp.setIconSize(QtCore.QSize(190, 74))
        self.cwp.setObjectName("cwp")
        self.aim = QtWidgets.QPushButton(Dialog)
        self.aim.setGeometry(QtCore.QRect(260, 260, 181, 23))
        self.aim.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.aim.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(resource_path("bin/img/settings/aim.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.aim.setIcon(icon1)
        self.aim.setIconSize(QtCore.QSize(193, 150))
        self.aim.setObjectName("aim")
        self.save = QtWidgets.QPushButton(Dialog)
        self.save.setGeometry(QtCore.QRect(156, 350, 181, 51))
        self.save.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.save.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(resource_path("bin/img/settings/save.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.save.setIcon(icon2)
        self.save.setIconSize(QtCore.QSize(193, 150))
        self.save.setObjectName("save")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(40, 110, 401, 31))
        self.label.setCursor(QtGui.QCursor(QtCore.Qt.ForbiddenCursor))
        self.label.setText("")
        self.label.setObjectName("label")
        self.unable_1 = QtWidgets.QLabel(Dialog)
        self.unable_1.setGeometry(QtCore.QRect(60, 160, 401, 31))
        self.unable_1.setCursor(QtGui.QCursor(QtCore.Qt.ForbiddenCursor))
        self.unable_1.setText("")
        self.unable_1.setObjectName("unable_1")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(140, 270, 51, 21))
        self.label_2.setCursor(QtGui.QCursor(QtCore.Qt.ForbiddenCursor))
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(70, 270, 51, 21))
        self.label_3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.label_3.setMouseTracking(False)
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.character_label = QtWidgets.QLabel(Dialog)
        self.character_label.setGeometry(QtCore.QRect(253, 302, 119, 16))
        font = QtGui.QFont()
        font.setFamily("Futura-Normal")
        font.setPointSize(12)
        self.character_label.setFont(font)
        self.character_label.setStyleSheet("color: orange;")
        self.character_label.setAlignment(QtCore.Qt.AlignCenter)
        self.character_label.setObjectName("character_label")
        self.character_change = QtWidgets.QPushButton(Dialog)
        self.character_change.setGeometry(QtCore.QRect(377, 296, 65, 26))
        self.character_change.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.character_change.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(resource_path("bin/img/settings/change.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.character_change.setIcon(icon3)
        self.character_change.setIconSize(QtCore.QSize(193, 150))
        self.character_change.setObjectName("character_change")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.character_label.setText(_translate("Dialog", "Choose character"))


