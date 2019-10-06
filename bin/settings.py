from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSlot
from bin.gnome import GnomeDialog
from bin.Qt.settings_Qt import Ui_Dialog as Ui_SettingsDialog
from bin.wow import wow_config as wow_folder
from db_connect import Database
from bin.resource_to_exe import resource_path

DB = Database()

class SettingsDialog(QtWidgets.QDialog):
    def __init__(self, main, character, parent=None):
        super(SettingsDialog, self).__init__(parent)
        self.ui = Ui_SettingsDialog()
        self.oldPos = self.pos()
        self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(resource_path('bin\\img\\settings.png')))
        self.main = main
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.GnomeDialog = None
        self.GnomeAwaits = None
        self.ui.aim.setCursor(QtGui.QCursor(QtCore.Qt.ForbiddenCursor))
        self.ui.aim.setToolTip('The addon will be installed automatically after setting the character and WoW path')
        self.wow_path = DB.query('SELECT data FROM system where variable="wow_path"')[0][0]
        self.ui.cwp.clicked.connect(self.cwp)
        self.ui.save.clicked.connect(self.save)
        self.ui.character_label.setText(character)
        self.ui.character_change.clicked.connect(self.character_change)
        if self.wow_path is None:
            self.GnomeDialog = GnomeDialog(14, '\n\n\nClick "Choose WoW path"!')
            self.GnomeDialog.show()
            self.GnomeAwaits = self.cwp.__name__

    def character_change(self):
        if not self.GnomeDialog:
            self.GnomeDialog = GnomeDialog(main=self, _type='account', DB=DB, wow_path=self.wow_path, settings=self)
            self.GnomeDialog.show()

    def save(self):
        if self.main is not None:
            self.main.show()
        self.close()

    def cwp(self):
        if self.GnomeDialog is not None and self.GnomeAwaits != self.cwp.__name__:
            self.GnomeDialog.ui.bg.setPixmap(QtGui.QPixmap(resource_path("bin/img/gnome/nani.png")))
            return
        elif self.GnomeDialog is not None:
            self.GnomeDialog.close()
        wow_path = QtWidgets.QFileDialog.getOpenFileName(
            parent=self,
            caption='Select your Wow.exe',
            filter="Wow*.exe")[0]
        if 'exe' not in wow_path:
            return
        DB.query(f'UPDATE system SET data=? WHERE variable="wow_path"', (wow_path,))
        DB.commit()
        wow_folder.default_config(self.main, GnomeDialog, wow_path)
        if self.main.GnomeDialog:
            self.main.GnomeDialog = None
        # TODO Проверить аддон, загрузить, если его нет, настроить ТМВ, переписать конфиг




    @pyqtSlot()
    def _exit(self):
        self.close()

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QtCore.QPoint(event.globalPos() - self.oldPos)
        # print(delta)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()