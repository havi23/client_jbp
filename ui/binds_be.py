from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSlot
from ui.binds import Ui_Dialog as Ui_BindsDialog_
from db_connect import Database

DB = Database()


class BindsDialog(QtWidgets.QDialog):
    # clicked = QtCore.pyqtSignal(str)
    def __init__(self, main, parent=None):
        super(BindsDialog, self).__init__(parent)
        self.oldPos = self.pos()
        self.ui = Ui_BindsDialog_()
        self.ui.setupUi(self)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.ui.scrollArea.setStyleSheet("background-color:transparent;")
        possible_binds = ['None', 'F1', 'F2', 'F3']
        self.ui.combo_1.addItems(possible_binds)
        self.ui.combo_1.setStyleSheet('color: red;')
        abils = DB.query("select * from sub")
        for idx, abil in enumerate(abils, start=1):
            exec(f'self.ui.combo_{idx} = QtWidgets.QComboBox(self.ui.formLayoutWidget)')
            exec(f'self.ui.combo_{idx}.setMinimumSize(QtCore.QSize(0, 28))')
            exec(f'self.ui.combo_{idx}.setObjectName(f"combo_{idx}")')
            exec(f'self.ui.combo_{idx}.addItems(possible_binds)')
            exec(f'self.ui.combo_{idx}.setStyleSheet("color: red;")')
            exec(f'self.ui.formLayout.setWidget({idx}, QtWidgets.QFormLayout.LabelRole, self.ui.combo_{idx})')
            exec(f'self.ui.text_{idx} = QtWidgets.QLabel(self.ui.formLayoutWidget)')
            exec(f'self.ui.text_{idx}.setFont(self.ui.font)')
            exec(f'self.ui.text_{idx}.setStyleSheet("color: silver;")')
            exec(f'self.ui.text_{idx}.setObjectName("text_{idx}")')
            exec(f'self.ui.formLayout.setWidget({idx}, QtWidgets.QFormLayout.FieldRole, self.ui.text_{idx})')



# TODO узнать что под мышкой и переместить
'''
    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QtCore.QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()
'''
