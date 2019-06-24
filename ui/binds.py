# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'binds.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(554, 535)
        self.bg = QtWidgets.QLabel(Dialog)
        self.bg.setGeometry(QtCore.QRect(30, 0, 501, 531))
        self.bg.setText("")
        self.bg.setPixmap(QtGui.QPixmap("ui/img/binds/binds_bg.png"))
        self.bg.setObjectName("bg")
        self.scrollArea = QtWidgets.QScrollArea(Dialog)
        self.scrollArea.setGeometry(QtCore.QRect(40, 60, 481, 371))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 479, 369))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.formLayoutWidget = QtWidgets.QWidget(self.scrollAreaWidgetContents)
        self.formLayoutWidget.setGeometry(QtCore.QRect(0, 0, 481, 371))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.FieldsStayAtSizeHint)
        self.formLayout.setRowWrapPolicy(QtWidgets.QFormLayout.DontWrapRows)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.combo_1 = QtWidgets.QComboBox(self.formLayoutWidget)
        self.combo_1.setMinimumSize(QtCore.QSize(0, 28))
        self.combo_1.setObjectName("combo_1")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.combo_1)
        self.text_1 = QtWidgets.QLabel(self.formLayoutWidget)
        self.font = QtGui.QFont()
        self.font.setFamily("Futura-Normal")
        self.font.setPointSize(22)
        self.font.setBold(False)
        self.font.setItalic(False)
        self.font.setUnderline(False)
        self.font.setWeight(50)
        self.font.setStrikeOut(False)
        self.font.setKerning(True)
        self.text_1.setFont(self.font)
        self.text_1.setStyleSheet("color: silver;")
        self.text_1.setObjectName("text_1")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.text_1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.text_1.setText(_translate("Dialog", "TextLabel"))


