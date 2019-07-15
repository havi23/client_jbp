# -*- coding: utf-8 -*-

# Form implementation generated from reading bin file 'binds.bin'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from db_connect import Database

DB = Database()

class Ui_Dialog(object):
    def setupUi(self, Dialog, spec):
        Dialog.setObjectName("Dialog")
        Dialog.resize(554, 535)
        self.bg = QtWidgets.QLabel(Dialog)
        self.bg.setGeometry(QtCore.QRect(30, 0, 501, 531))
        self.bg.setText("")
        self.bg.setPixmap(QtGui.QPixmap("bin/img/binds/binds_bg.png"))
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
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setRowWrapPolicy(QtWidgets.QFormLayout.DontWrapRows)
        self.formLayout.setContentsMargins(3, 3, 3, 3)
        self.formLayout.setObjectName("formLayout")
        #QtWidgets.QAbstractScrollArea.setVerticalScrollBarPolicy(self.scrollArea, Qt.ScrollBarAlwaysOn)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        font = QtGui.QFont()
        font.setFamily("Futura-Normal")
        font.setPointSize(22)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(True)
        possible_binds = ['None', 'F1', 'F2', 'F3']
        abils = DB.query(f"select * from {spec}")
        print(len(abils))
        for idx, abil in enumerate(abils, start=1):
            exec(f'self.combo_{idx} = QtWidgets.QComboBox(self.formLayoutWidget)')
            exec(f'self.combo_{idx}.setMinimumSize(QtCore.QSize(0, 28))')
            exec(f'self.combo_{idx}.setObjectName("combo_{idx}")')
            exec(f'self.formLayout.setWidget({idx}+1, QtWidgets.QFormLayout.LabelRole, self.combo_{idx})')
            exec(f'self.text_{idx} = QtWidgets.QLabel(self.formLayoutWidget)')
            exec(f'self.text_{idx}.setFont(font)')
            exec(f'self.text_{idx}.setStyleSheet("color: silver;")')
            exec(f'self.text_{idx}.setObjectName("text_{idx}")')
            exec(f'self.text_{idx}.setMinimumSize(QtCore.QSize(0, 28))')
            exec(f'self.formLayout.setWidget({idx}+1, QtWidgets.QFormLayout.FieldRole, self.text_{idx})')
            exec(f'self.scrollArea.setWidget(self.scrollAreaWidgetContents)')
            exec(f'self.combo_{idx}.addItems(possible_binds)')
            exec(f'self.combo_{idx}.setStyleSheet("color: red;")')
            self.count = idx
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        for i in range(1, self.count+1):
            exec(f'self.text_{i}.setText(_translate("Dialog", "TextLabel"))')


