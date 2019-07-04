from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSlot
from ui.bug_report import Ui_Dialog as Ui_BugReportDialog


class BugReportDialog(QtWidgets.QDialog):
    def __init__(self, main=None, parent=None):
        super(BugReportDialog, self).__init__(parent)
        self.main = main
        self.main.hide()
        self.oldPos = self.pos()
        self.ui = Ui_BugReportDialog()
        self.ui.setupUi(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground | QtCore.Qt.WA_TranslucentBackground)
        self.ui.close_.mousePressEvent = lambda event: self._exit(main)
        self.ui.choose_screen.clicked.connect(self.scr_attach)
        self.ui.send.clicked.connect(self.send)
        self.attachments = list()

    def send(self, main):
        print(self.attachments)

    def scr_attach(self):
        count = self.ui.scr_count.intValue()
        if count < 9:
            scr_path = QtWidgets.QFileDialog.getOpenFileName(
                parent=self,
                caption='Attach an image',
                filter="Image Files(*.png *.jpg *.kek)")[0]
            q_file = QtCore.QFile(scr_path)
            if q_file.exists():
                if scr_path[-3:] == 'kek':
                    from db_connect import Database
                    DB = Database()
                    site_name = DB.query('select data from system where variable="site_name"')[0][0]
                    current_text = self.ui.text.toPlainText()
                    gift = 'AF63D1C-03D712-D12734'#  TODO Gift post
                    self.ui.text.setText(f'{gift}'
                                         f'\n/\ This is your gift promo code for a 20% discount on {site_name}'
                                         f'\n\nhttps://kekopedia.fandom.com/ru/wiki/Кек?file=Кек1.jpg'
                                         f'\n\n{current_text}')
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

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            event.ignore()
        elif event.key() == QtCore.Qt.Key_Enter:
            self.send(self.main)

    @pyqtSlot()
    def _exit(self, main):
        if main:
            main.GnomeDialog = None
            main.show()
        self.close()
