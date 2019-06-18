from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSlot
from ui.main_window import Ui_Dialog as Ui_MainDialog
import sys


class MainDialog(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainDialog, self).__init__(parent)
        self.GnomeDialog = None
        self.oldPos = self.pos()
        self.ui = Ui_MainDialog()
        self.ui.setupUi(self)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        #self.setFixedSize(695, 577)
        self.ui.binds.clicked.connect(self.binds)
        self.ui.close.clicked.connect(self.close)
        self.ui.change_class.clicked.connect(self.change_class)

    @pyqtSlot()
    def binds(self):
        if not self.GnomeDialog:
            self.GnomeDialog = GnomeDialog(self, 16, 'Hello, my Friend!\n\n'
                        'My name is Ho Linka and today i will help you to setup your routine.\n\n'
                        '')
        self.GnomeDialog.show()

    @pyqtSlot()
    def change_class(self):
        print('test')
    @pyqtSlot()
    def close(self):
        sys.exit()

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()
    def mouseMoveEvent(self, event):
        delta = QtCore.QPoint(event.globalPos() - self.oldPos)
        # print(delta)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

class MainDialog(QtWidgets.QDialog):
    # clicked = QtCore.pyqtSignal(str)
    def __init__(self, size, text, parent=None):
        super(MainDialog, self).__init__(parent)
        self.ui = Ui_MainDialog()
        self.ui.setupUi(self)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setFixedSize(695, 577)
        ag = QtWidgets.QDesktopWidget().availableGeometry()
        sg = QtWidgets.QDesktopWidget().screenGeometry()
        widget = self.geometry()
        x = ag.width() - widget.width()
        y = 2 * ag.height() - sg.height() - widget.height()
        self.move(x, y)

        self.ui.okay.clicked.connect(self._exit)
        self.ui.text.setFont(QtGui.QFont("Times", size, QtGui.QFont.StyleItalic))
        self.ui.text.setAlignment(QtCore.Qt.AlignTop| QtCore.Qt.AlignHCenter)
        self.ui.text.setText(text)

    @pyqtSlot()
    def _exit(self):
        self.close()

app = QtWidgets.QApplication([])
#gnome = GnomeDialog(16, 'Hello, my Friend!\n\n'
#                       'My name is Ho Linka and today i will help you to setup your routine.\n\n'
#                        '')
#gnome.show()
main = MainDialog()
main.show()
sys.exit(app.exec())