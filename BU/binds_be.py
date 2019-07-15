from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSlot
from bin.binds import Ui_Dialog as Ui_BindsDialog_
from db_connect import Database

DB = Database()


class BindsDialog(QtWidgets.QDialog):
    # clicked = QtCore.pyqtSignal(str)
    def __init__(self, main, spec, parent=None):
        super(BindsDialog, self).__init__(parent)
        self.oldPos = self.pos()
        self.ui = Ui_BindsDialog_(self, spec)
        #self.bin.setupUi()#, spec)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        #self.bin.scrollArea.setStyleSheet("background-color:transparent;")
        '''
        possible_binds = ['None', 'F1', 'F2', 'F3']
        self.bin.combo_1.addItems(possible_binds)
        self.bin.combo_1.setStyleSheet('color: red;')
        abils = DB.query("select * from ?", spec)
        print(abils)
        for idx, abil in enumerate(abils, start=1):
            exec(f'self.bin.combo_{idx} = QtWidgets.QComboBox(self.bin.formLayoutWidget)')
            exec(f'self.bin.combo_{idx}.setMinimumSize(QtCore.QSize(0, 28))')
            exec(f'self.bin.combo_{idx}.setObjectName(f"combo_{idx}")')
            exec(f'self.bin.combo_{idx}.addItems(possible_binds)')
            exec(f'self.bin.combo_{idx}.setStyleSheet("color: red;")')
            exec(f'self.bin.formLayout.setWidget({idx}, QtWidgets.QFormLayout.LabelRole, self.bin.combo_{idx})')
            exec(f'self.bin.text_{idx} = QtWidgets.QLabel(self.bin.formLayoutWidget)')
            exec(f'self.bin.text_{idx}.setFont(self.bin.font)')
            exec(f'self.bin.text_{idx}.setStyleSheet("color: silver;")')
            exec(f'self.bin.text_{idx}.setObjectName("text_{idx}")')
            exec(f'self.bin.formLayout.setWidget({idx}, QtWidgets.QFormLayout.FieldRole, self.bin.text_{idx})')
'''


# TODO узнать что под мышкой и переместить
'''
    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QtCore.QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()
'''
