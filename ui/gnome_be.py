from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSlot
from ui.gnome import Ui_Dialog as Ui_GnomeDialog


class GnomeDialog(QtWidgets.QDialog):
    # clicked = QtCore.pyqtSignal(str)
    def __init__(self, size, text, button=None, parent=None):
        super(GnomeDialog, self).__init__(parent)
        self.ui = Ui_GnomeDialog()
        self.ui.setupUi(self)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool)
        ag = QtWidgets.QDesktopWidget().availableGeometry()
        sg = QtWidgets.QDesktopWidget().screenGeometry()
        widget = self.geometry()
        x = ag.width() - widget.width()
        y = 2 * ag.height() - sg.height() - widget.height()
        self.move(x, y)
        self.ui.text.setFont(QtGui.QFont("Times", size, QtGui.QFont.StyleItalic))
        self.ui.text.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)
        self.ui.text.setText(text)
        if button:
            self.ui.okay.clicked.connect(self._exit)
        else:
            self.ui.okay.hide()

    @pyqtSlot()
    def _exit(self):
        self.close()

