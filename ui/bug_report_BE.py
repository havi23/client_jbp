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
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground | QtCore.Qt.WA_TranslucentBackground)
        self.ui.close_.mousePressEvent = lambda event: self._exit(main)
        self.ui.choose_screen.clicked.connect(self.scr_attach)
        self.ui.send.clicked.connect(self.send)
        self.attachments = list()

    def send(self):
        print(self.attachments)

    def scr_attach(self):
        count = self.ui.scr_count.intValue()
        if count < 9:
            scr_path = QtWidgets.QFileDialog.getOpenFileName(
                parent=self,
                caption='Attach screenshot',
                filter="Image Files(*.png *.jpg *.bmp)")[0]
            print(scr_path)
            with open(scr_path, mode='rb') as file:
                self.attachments.append(file.read()) #  Добавление файла(битами) в массив
            if count == 8: #  9 - ограничитель
                self.ui.scr_count.setStyleSheet('background-color: red;')
                self.ui.choose_screen.setVisible(0)
                self.ui.label_tooltip.setText('It is maximum.')
            self.ui.scr_count.display(count + 1)

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
