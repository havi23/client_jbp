# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'bug_report.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(972, 802)
        font = QtGui.QFont()
        font.setFamily("Futura")
        font.setPointSize(10)
        Dialog.setFont(font)
        self.bg = QtWidgets.QLabel(Dialog)
        self.bg.setGeometry(QtCore.QRect(350, 290, 281, 261))
        self.bg.setText("")
        self.bg.setPixmap(QtGui.QPixmap("ui/img/bug_report.png"))
        self.bg.setObjectName("bg")
        self.send = QtWidgets.QPushButton(Dialog)
        self.send.setGeometry(QtCore.QRect(563, 520, 61, 21))
        font = QtGui.QFont()
        font.setFamily("Futura-Normal")
        font.setPointSize(10)
        self.send.setFont(font)
        self.send.setStyleSheet("    color: #fff;\n"
"    border: 1px solid #00aeff;\n"
"    box-shadow: 3px 3px 3px rgba(0, 0, 0, 0.3);\n"
"    background-color: #0e86ca;\n"
"    transition: color .2s,background-color .2s,border-color .2s;\n"
"    cursor: pointer;\n"
"    max-width: 100%;\n"
"    white-space: normal")
        self.send.setObjectName("send")
        self.text = QtWidgets.QTextEdit(Dialog)
        self.text.setGeometry(QtCore.QRect(360, 338, 265, 178))
        font = QtGui.QFont()
        font.setFamily("Futura-Normal")
        font.setPointSize(11)
        self.text.setFont(font)
        self.text.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.text.setMouseTracking(False)
        self.text.setAutoFillBackground(False)
        self.text.setStyleSheet("background-color: rgba(0,0,0,50%); color : red;")
        self.text.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.text.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.text.setOverwriteMode(False)
        self.text.setObjectName("text")
        self.choose_screen = QtWidgets.QToolButton(Dialog)
        self.choose_screen.setGeometry(QtCore.QRect(531, 521, 26, 19))
        self.choose_screen.setStyleSheet("    color: #fff;\n"
"    border: 1px solid #00aeff;\n"
"    box-shadow: 3px 3px 3px rgba(0, 0, 0, 0.3);\n"
"    background-color: #0e86ca;\n"
"    transition: color .2s,background-color .2s,border-color .2s;\n"
"    cursor: pointer;\n"
"    max-width: 100%;\n"
"    white-space: normal")
        self.choose_screen.setObjectName("choose_screen")
        self.label_tooltip = QtWidgets.QLabel(Dialog)
        self.label_tooltip.setGeometry(QtCore.QRect(362, 519, 171, 20))
        self.label_tooltip.setMaximumSize(QtCore.QSize(173, 16777215))
        self.label_tooltip.setStyleSheet("color: #0e86ca;")
        self.label_tooltip.setObjectName("label_tooltip")
        self.close_ = QtWidgets.QLabel(Dialog)
        self.close_.setGeometry(QtCore.QRect(582, 308, 38, 16))
        self.close_.setText("")
        self.close_.setObjectName("close_")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.send.setText(_translate("Dialog", "SEND"))
        self.text.setPlaceholderText(_translate("Dialog", "Write a descriprion of your problem here..."))
        self.choose_screen.setText(_translate("Dialog", "..."))
        self.label_tooltip.setText(_translate("Dialog", "Here you can attach a screen"))


