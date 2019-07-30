from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSlot
from bin.Qt.class_Qt import Ui_Dialog as Ui_SpecDialog
from bin.Qt.spec_Qt import Ui_Dialog as Ui_SpecDialog_
from db_connect import Database
from bin.gnome import GnomeDialog
from bin.resource_to_exe import resource_path

DB = Database()

class SpecDialog(QtWidgets.QDialog):
    # clicked = QtCore.pyqtSignal(str)
    def __init__(self, main, class_, parent=None):
        super(SpecDialog, self).__init__(parent)
        self.oldPos = self.pos()
        self.ui = Ui_SpecDialog_()
        print(class_)
        self.ui.setupUi(self)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.ui.bg.setPixmap(QtGui.QPixmap(resource_path(f"bin/img/class/spec/spec_{class_}.png")))
        self.GnomeDialog = None
        #QtGui.QMouseEvent
        if class_ not in ('Demon_Hunter', 'Druid'):
            self.ui.spec_1_.close()
            self.ui.spec_2_.close()
            self.ui.spec_3_.close()
            self.ui.spec_4_.close()
            self.ui.spec_1.mouseReleaseEvent = lambda event: self.spec(main, class_, 1)  # У друида и ДХ не по 3 спека
            self.ui.spec_2.mouseReleaseEvent = lambda event: self.spec(main, class_, 2)
            self.ui.spec_3.mouseReleaseEvent = lambda event: self.spec(main, class_, 3)
            self.ui.spec_1.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            self.ui.spec_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            self.ui.spec_3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        else:
            self.ui.spec_1.close()
            self.ui.spec_2.close()
            self.ui.spec_3.close()
            self.ui.spec_1_.mouseReleaseEvent = lambda event: self.spec(main, class_, 1)  # 1-4 у друида, 2-3 у ДХ
            self.ui.spec_2_.mouseReleaseEvent = lambda event: self.spec(main, class_, 2)
            self.ui.spec_3_.mouseReleaseEvent = lambda event: self.spec(main, class_, 3)
            self.ui.spec_4_.mouseReleaseEvent = lambda event: self.spec(main, class_, 4)
            self.ui.spec_2_.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            self.ui.spec_3_.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            if class_ == 'Druid':
                self.ui.spec_1_.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                self.ui.spec_4_.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            else:
                self.ui.spec_1_.close()
                self.ui.spec_4_.close()

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QtCore.QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

    def spec(self, main, class_, spec):
        spec = DB.query(f'select * from specs where class="{class_}";')[0][spec]
        if spec not in main.options:
            if self.GnomeDialog is None:
                self.GnomeDialog = GnomeDialog(14, f"\n\nYou dont have this spec on your key\n"
                                                   "You can buy it on our Web-Site", True, self)
                self.GnomeDialog.show()
            return
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
        self.ui.dh.clicked.connect(lambda: self.choose_spec(main, 'Demon_Hunter'))
        self.ui.dk.clicked.connect(lambda: self.choose_spec(main, 'Death_Knight'))
        self.ui.dru.clicked.connect(lambda: self.choose_spec(main, 'Druid'))
        self.ui.hun.clicked.connect(lambda: self.choose_spec(main, 'Hunter'))
        self.ui.mag.clicked.connect(lambda: self.choose_spec(main, 'Mage'))
        self.ui.mon.clicked.connect(lambda: self.choose_spec(main, 'Monk'))
        self.ui.pal.clicked.connect(lambda: self.choose_spec(main, 'Paladin'))
        self.ui.pri.clicked.connect(lambda: self.choose_spec(main, 'Priest'))
        self.ui.rog.clicked.connect(lambda: self.choose_spec(main, 'Rogue'))
        self.ui.sha.clicked.connect(lambda: self.choose_spec(main, 'Shaman'))
        self.ui.warr.clicked.connect(lambda: self.choose_spec(main, 'Warrior'))
        self.ui.warl.clicked.connect(lambda: self.choose_spec(main, 'Warlock'))

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
            self.hide()

    @pyqtSlot()
    def back(self, main):
        if main is not None:
            main.show()
        self.close()