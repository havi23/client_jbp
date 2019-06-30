from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSlot
from ui.bug_report import Ui_Dialog as Ui_BugReportDialog


class BugReportDialog(QtWidgets.QDialog):
    def __init__(self, main=None, parent=None):
        super(BugReportDialog, self).__init__(parent)
        main.hide()
        self.oldPos = self.pos()
        self.ui = Ui_BugReportDialog()
        self.ui.setupUi(self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool)
        self.ui.close_.mousePressEvent = lambda event: self._exit(main)
    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QtCore.QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

    @pyqtSlot()
    def _exit(self, main):
        if main:
            main.GnomeDialog = None
        main.show()
        self.close()
