# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gnome.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from ui.resource_to_exe import resource_path

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(695, 577)
        self.bg = QtWidgets.QLabel(Dialog)
        self.bg.setGeometry(QtCore.QRect(220, 110, 471, 471))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bg.sizePolicy().hasHeightForWidth())
        self.bg.setSizePolicy(sizePolicy)
        self.bg.setText("")
        self.bg.setPixmap(QtGui.QPixmap(resource_path("ui/img/gnome/empty.png")))
        self.bg.setScaledContents(True)
        self.bg.setAlignment(QtCore.Qt.AlignCenter)
        self.bg.setWordWrap(False)
        self.bg.setOpenExternalLinks(False)
        self.bg.setObjectName("bg")
        self.text = QtWidgets.QLabel(Dialog)
        self.text.setGeometry(QtCore.QRect(240, 130, 311, 221))
        self.text.setText("")
        self.text.setTextFormat(QtCore.Qt.PlainText)
        self.text.setScaledContents(False)
        self.text.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.text.setWordWrap(True)
        self.text.setOpenExternalLinks(False)
        self.text.setObjectName("text")
        self.okay = QtWidgets.QPushButton(Dialog)
        self.okay.setGeometry(QtCore.QRect(340, 330, 111, 31))
        self.okay.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.okay.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(resource_path("ui/img/gnome/okdok1.bmp")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.okay.setIcon(icon)
        self.okay.setIconSize(QtCore.QSize(180, 90))
        self.okay.setShortcut("")
        self.okay.setCheckable(False)
        self.okay.setAutoRepeat(False)
        self.okay.setAutoExclusive(False)
        self.okay.setFlat(True)
        self.okay.setObjectName("okay")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))


