from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSlot
from ui.spec import Ui_Dialog as Ui_SpecDialog
from ui.spec_ import Ui_Dialog as Ui_SpecDialog_
from db_connect import Database


DB = Database()

class SpecDialog(QtWidgets.QDialog):
    # clicked = QtCore.pyqtSignal(str)
    def __init__(self, main, class_, parent=None):
        super(SpecDialog, self).__init__(parent)
        self.oldPos = self.pos()
        self.ui = Ui_SpecDialog_()
        self.ui.setupUi(self)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.ui.bg.setPixmap(QtGui.QPixmap(f"ui/img/class/spec/spec_{class_}.png"))
        #QtGui.QMouseEvent
        if class_ not in ('dh', 'dru'):
            self.ui.spec_1.mousePressEvent = lambda event: self.spec(main, class_, 1)  # У друида и ДХ не по 3 спека
            self.ui.spec_2.mousePressEvent = lambda event: self.spec(main, class_, 2)
            self.ui.spec_3.mousePressEvent = lambda event: self.spec(main, class_, 3)
        else:
            self.ui.spec_1.close()
            self.ui.spec_2.close()
            self.ui.spec_3.close()
            self.ui.spec_1_.mousePressEvent = lambda event: self.spec(main, class_, 1)  # 1-4 у друида, 2-3 у ДХ
            self.ui.spec_2_.mousePressEvent = lambda event: self.spec(main, class_, 2)
            self.ui.spec_3_.mousePressEvent = lambda event: self.spec(main, class_, 3)
            self.ui.spec_4_.mousePressEvent = lambda event: self.spec(main, class_, 4)

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QtCore.QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

    def spec(self, main, class_, spec):
        spec = DB.query(f'select * from specs where class="{class_}";')[0][spec]
        DB.query(f'update system set data = "{spec}" where variable ="spec";')
        DB.query(f'update system set data = "{class_}" where variable ="class";')
        DB.commit()
        if main is not None:
            main.show()
        self.close()


class ClassDialog(QtWidgets.QDialog):
    # clicked = QtCore.pyqtSignal(str)
    def __init__(self, main=None, parent=None):
        super(ClassDialog, self).__init__(parent)
        self.oldPos = self.pos()
        self.ui = Ui_SpecDialog()
        self.ui.setupUi(self)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.ui.dh.clicked.connect(lambda: self.choose_spec(main, 'dh'))
        self.ui.dk.clicked.connect(lambda: self.choose_spec(main, 'dk'))
        self.ui.dru.clicked.connect(lambda: self.choose_spec(main, 'dru'))
        self.ui.hun.clicked.connect(lambda: self.choose_spec(main, 'hun'))
        self.ui.mag.clicked.connect(lambda: self.choose_spec(main, 'mag'))
        self.ui.mon.clicked.connect(lambda: self.choose_spec(main, 'mon'))
        self.ui.pal.clicked.connect(lambda: self.choose_spec(main, 'pal'))
        self.ui.pri.clicked.connect(lambda: self.choose_spec(main, 'pri'))
        self.ui.rog.clicked.connect(lambda: self.choose_spec(main, 'rog'))
        self.ui.sha.clicked.connect(lambda: self.choose_spec(main, 'sha'))
        self.ui.warr.clicked.connect(lambda: self.choose_spec(main, 'warr'))
        self.ui.warl.clicked.connect(lambda: self.choose_spec(main, 'warl'))

        self.SpecDialog = None
    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QtCore.QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

    @pyqtSlot()
    def choose_spec(self, main, class_):
        if self.SpecDialog is None:
            self.SpecDialog = SpecDialog(main, class_)
            self.SpecDialog.show()
            self.close()

    @pyqtSlot()
    def back(self, main):
        if main is not None:
            main.show()
        self.close()