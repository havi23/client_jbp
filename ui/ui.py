from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSlot
from ui.gnome import Ui_Dialog as Ui_GnomeDialog
from ui.main_window import Ui_Dialog as Ui_MainDialog
from ui.spec_be import ClassDialog
import sys
from db_connect import Database
import time

DB = Database()

#  pyuic5 main_window.ui -o main_window.py



class GnomeDialog(QtWidgets.QDialog):
    # clicked = QtCore.pyqtSignal(str)
    def __init__(self, size, text, button=None, parent=None):
        super(GnomeDialog, self).__init__(parent)
        self.ui = Ui_GnomeDialog()
        self.ui.setupUi(self)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
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

class MainDialog(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainDialog, self).__init__(parent)
        self.oldPos = self.pos()
        self.ui = Ui_MainDialog()
        self.ui.setupUi(self)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.ui.binds.clicked.connect(self.binds)
        self.ui.close.clicked.connect(self.close)
        self.ui.change_class.clicked.connect(self.change_class)
        self.ui.settings.clicked.connect(self.settings)
        self.ui.start.clicked.connect(self.start)
        #QtWidgets.qApp.processEvents()

    def event(self, event):  # Срабатывает при каждом вызове main.show()
        if event.type() == QtCore.QEvent.Show:
            self.GnomeDialog = None
            self.GnomeAwaits = None
            self.ClassDialog = None
            self.wow_path = DB.query('SELECT data FROM system where variable="wow_path"')[0][0]
            self.spec = DB.query('SELECT data FROM system where variable="spec"')[0][0]
            self.class_= DB.query('SELECT data FROM system where variable="class"')[0][0]
            if self.class_ is not None:
                self.ui.label.setPixmap(QtGui.QPixmap(f"ui/img/{self.class_}.png"))
            if self.wow_path is None:
                if not self.GnomeDialog:
                    self.GnomeDialog = GnomeDialog(14, 'Hello, my Friend!\n\n'
                                                       'My name is Ho Linka and today i will help you to setup your routine.\n'
                                                       'First of all I need to know where your WoW client is.\n\n'
                                                       'Click "Settings"!')
                self.GnomeDialog.show()
                self.GnomeAwaits = 'settings'

            elif self.spec is None:
                if not self.GnomeDialog:
                    self.GnomeDialog = GnomeDialog(14, 'Now you need to choose your class and specialisation\n\n\n'
                                                       'Click "Class"!')
                    self.GnomeDialog.show()
                    self.GnomeAwaits = 'change_class'
            elif self.spec is not None:
                binds = DB.query(f'SELECT * FROM {self.spec}')
                for bind in binds:
                    if bind[3] and bind[2] is None:
                        if not self.GnomeDialog:
                            self.GnomeDialog = GnomeDialog(14,
                                                           f'У тебя нет бинда на обязательной клавише: {bind[0]}\n\n'
                                                           'Click "Binds"!')
                        self.GnomeDialog.show()
                        self.GnomeAwaits = 'binds'
                        break
        return super(MainDialog, self).event(event)

    def binds(self):
        if self.GnomeDialog is not None and self.GnomeAwaits != self.binds.__name__:
            self.GnomeDialog.ui.bg.setPixmap(QtGui.QPixmap("ui/img/gnome/nani.png"))
            return
        pass

    def start(self):
        if self.GnomeDialog is not None and self.GnomeAwaits != self.start.__name__:
            self.GnomeDialog.ui.bg.setPixmap(QtGui.QPixmap("ui/img/gnome/nani.png"))
            return
        pass

    def settings(self):
        if self.GnomeDialog:
            self.GnomeDialog.close()
            self.GnomeDialog = None
            wow_path = QtWidgets.QFileDialog.getOpenFileName(parent=self, caption='Select your Wow.exe', filter="Wow*.exe")[0]
            DB.query(f'UPDATE system SET data="{wow_path}" WHERE variable="wow_path"')
            DB.commit()
            print(wow_path)
            print('Настройки с автогномом')
        else:
            print('Настройки без автогнома')

    def change_class(self):
        if self.GnomeDialog is not None and self.GnomeAwaits != self.change_class.__name__:
            self.GnomeDialog.ui.bg.setPixmap(QtGui.QPixmap("ui/img/gnome/nani.png"))
            return
        self.hide()
        if self.GnomeDialog is not None:
            self.GnomeDialog.close()
        self.ClassDialog = ClassDialog(self)
        self.ClassDialog.show()


    def close(self):
        sys.exit()

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QtCore.QPoint(event.globalPos() - self.oldPos)
        # print(delta)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()



'''
gnome = GnomeDialog(16, 'Hello, my Friend!\n\n'
                       'My name is Ho Linka and today i will help you to setup your routine.\n\n'
                        '')
'''
#gnome.show()

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    main = MainDialog()
    main.show()
    sys.exit(app.exec())
