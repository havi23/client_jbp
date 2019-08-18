# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'bug_report.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(278, 262)
        font = QtGui.QFont()
        font.setFamily("Futura")
        font.setPointSize(10)
        Dialog.setFont(font)
        self.bg = QtWidgets.QLabel(Dialog)
        self.bg.setGeometry(QtCore.QRect(-2, 0, 281, 263))
        self.bg.setText("")
        self.bg.setPixmap(QtGui.QPixmap("bin/img/bug_report/bug_report.png"))
        self.bg.setObjectName("bg")
        self.send = QtWidgets.QPushButton(Dialog)
        self.send.setGeometry(QtCore.QRect(211, 237, 61, 19))
        font = QtGui.QFont()
        font.setFamily("Futura-Normal")
        font.setPointSize(10)
        self.send.setFont(font)
        self.send.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.send.setStyleSheet("    color: #fff;\n"
"    border: 1px solid #00aeff;\n"
"    box-shadow: 3px 3px 3px rgba(0, 0, 0, 0.3);\n"
"    background-color: #0e86ca;\n"
"    transition: color .2s,background-color .2s,border-color .2s;\n"
"    cursor: pointer;\n"
"    white-space: normal")
        self.send.setObjectName("send")
        self.text = QtWidgets.QTextEdit(Dialog)
        self.text.setGeometry(QtCore.QRect(8, 50, 265, 143))
        font = QtGui.QFont()
        font.setFamily("Futura-Normal")
        font.setPointSize(11)
        self.text.setFont(font)
        self.text.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.text.setMouseTracking(False)
        self.text.setAutoFillBackground(True)
        self.text.setStyleSheet("background-color: transparent;\n"
"    color: white;")
        self.text.setOverwriteMode(False)
        self.text.setObjectName("text")
        self.choose_screen = QtWidgets.QToolButton(Dialog)
        self.choose_screen.setGeometry(QtCore.QRect(10, 233, 21, 19))
        self.choose_screen.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.choose_screen.setStyleSheet("    color: #fff;\n"
"    border: 1px solid #00aeff;\n"
"    box-shadow: 3px 3px 3px rgba(0, 0, 0, 0.3);\n"
"    background-color: #0e86ca;\n"
"    transition: color .2s,background-color .2s,border-color .2s;\n"
"    cursor: pointer;\n"
"    ;\n"
"    white-space: normal")
        self.choose_screen.setObjectName("choose_screen")
        self.label_tooltip = QtWidgets.QLabel(Dialog)
        self.label_tooltip.setGeometry(QtCore.QRect(50, 232, 161, 20))
        self.label_tooltip.setMaximumSize(QtCore.QSize(173, 16777215))
        self.label_tooltip.setStyleSheet("color: #0e86ca;")
        self.label_tooltip.setObjectName("label_tooltip")
        self.close_ = QtWidgets.QLabel(Dialog)
        self.close_.setGeometry(QtCore.QRect(230, 20, 38, 16))
        self.close_.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.close_.setText("")
        self.close_.setObjectName("close_")
        self.scr_count = QtWidgets.QLCDNumber(Dialog)
        self.scr_count.setGeometry(QtCore.QRect(7, 230, 38, 25))
        self.scr_count.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.scr_count.setFrameShape(QtWidgets.QFrame.Box)
        self.scr_count.setFrameShadow(QtWidgets.QFrame.Raised)
        self.scr_count.setDigitCount(4)
        self.scr_count.setMode(QtWidgets.QLCDNumber.Dec)
        self.scr_count.setSegmentStyle(QtWidgets.QLCDNumber.Filled)
        self.scr_count.setObjectName("scr_count")
        self.len_limit = QtWidgets.QLabel(Dialog)
        self.len_limit.setGeometry(QtCore.QRect(217, 219, 53, 21))
        font = QtGui.QFont()
        font.setFamily("Futura")
        self.len_limit.setFont(font)
        self.len_limit.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.len_limit.setStyleSheet("color: rgba(150, 150, 150, 0.5);")
        self.len_limit.setAlignment(QtCore.Qt.AlignCenter)
        self.len_limit.setObjectName("len_limit")
        self.contact_type = QtWidgets.QComboBox(Dialog)
        self.contact_type.setGeometry(QtCore.QRect(190, 196, 82, 23))
        self.contact_type.setAutoFillBackground(False)
        self.contact_type.setStyleSheet("background: rgba(255,255,255, 0.5);")
        self.contact_type.setObjectName("contact_type")
        self.contact_text = QtWidgets.QLineEdit(Dialog)
        self.contact_text.setGeometry(QtCore.QRect(8, 197, 181, 22))
        self.contact_text.setStyleSheet("background-color: transparent;\n"
"    color: white;")
        self.contact_text.setInputMethodHints(QtCore.Qt.ImhMultiLine)
        self.contact_text.setObjectName("contact_text")
        self.bg.raise_()
        self.scr_count.raise_()
        self.send.raise_()
        self.text.raise_()
        self.choose_screen.raise_()
        self.label_tooltip.raise_()
        self.close_.raise_()
        self.len_limit.raise_()
        self.contact_type.raise_()
        self.contact_text.raise_()

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.send.setText(_translate("Dialog", "SEND"))
        self.text.setPlaceholderText(_translate("Dialog", "Write a descriprion of your problem here..."))
        self.choose_screen.setText(_translate("Dialog", "+"))
        self.label_tooltip.setText(_translate("Dialog", "You can attach a screenshot"))
        self.len_limit.setText(_translate("Dialog", "0/2000"))
        self.contact_text.setPlaceholderText(_translate("Dialog", "Your contact here..."))

