from PyQt5 import QtWidgets, QtCore, QtGui
from bin.gnome import GnomeDialog
from bin.Qt.main_window_Qt import Ui_Dialog as Ui_MainDialog
from bin.spec import ClassDialog
from bin.binds import Ui_Dialog as BindsDialog
from bin.bug_report import BugReportDialog
import sys
from db_connect import Database
from bin.settings import SettingsDialog
import time
import os
from bin.resource_to_exe import resource_path
from bin.wow import wow_config as wow_folder
from bin.wow.ahk_console import ahk_console
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
#  pyuic5 main_window.ui -o main_window_Qt.py


class MainDialog(QtWidgets.QMainWindow):
    def __init__(self, server, LicenseKeyDialog=None):
        super(MainDialog, self).__init__()
        self.DB = Database()
        self.server = server
        self.LicenseKeyDialog = LicenseKeyDialog
        if self.LicenseKeyDialog:
            self.LicenseKeyDialog.close()
        self.options = server.options
        self.options = self.options.split('|')
        print(self.options)
        self.wow_correct = None
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
        self.ui.start_wow.clicked.connect(self.start_wow)
        self.ui.bug_report.clicked.connect(self.bug_report)
        self.ui.reload.clicked.connect(self.relaod_UI)
        self.ui.wow_text.mouseReleaseEvent = lambda event: self.wow_text_tooltip()
        self.start_icon = QtGui.QIcon()
        self.start_icon.addPixmap(QtGui.QPixmap(resource_path("bin/img/main/start.bmp")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.stop_icon = QtGui.QIcon()
        self.stop_icon.addPixmap(QtGui.QPixmap(resource_path("bin/img/main/start.bmp")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.listener = None
        self.m_label = None
        self.info_active = None
        self.ui.info.clicked.connect(self.info_frame)
        self.GnomeDialog = None
        self.GnomeAwaits = None
        self.ClassDialog = None
        self.SettingsDialog = None
        self.BindsDialog = None
        self.BugReport = None

        # Обновление токена
        self.token_updater = BackgroundScheduler()
        trigger = IntervalTrigger(seconds=200)
        self.token_updater.add_job(lambda: server.token_update(self), trigger)
        self.token_updater.start()
        # self.token_updater - поток, в котором крутится обновление

    def info_frame(self):
        if self.info_active:
            icon4 = QtGui.QIcon()
            icon4.addPixmap(QtGui.QPixmap(resource_path("bin/img/main/info.bmp")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.info.setIcon(icon4)
            self.ui.label.setGeometry(QtCore.QRect(442, 255, 261, 461))
            if self.class_ is not None:
                self.ui.label.setPixmap(QtGui.QPixmap(resource_path(f'bin/img/main/{self.class_}.png')))
            else:
                self.ui.label.setPixmap(QtGui.QPixmap(resource_path(f'bin/img/main/noclass.png')))
            self.info_active = False
        else:
            icon4 = QtGui.QIcon()
            icon4.addPixmap(QtGui.QPixmap(resource_path("bin/img/main/info_c.bmp")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.info.setIcon(icon4)
            self.ui.label.setGeometry(QtCore.QRect(121, 7, 1021, 861))
            self.ui.label.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
            self.ui.label.setText("")
            self.ui.label.setPixmap(QtGui.QPixmap(resource_path("bin\\img\\main\\info_bg.png")))
            self.ui.label.setObjectName("info_bg")
            self.info_active = True

    def wow_text_tooltip(self):
        print('ОТКРОЕТСЯ САЙТ')

    def relaod_UI(self):
        self.check_wow()

    def bug_report(self):
        if not self.BugReport:
            self.BugReport = BugReportDialog(self)
            self.BugReport.show()


    def start_wow(self):
        self.check_wow()
        if self.wow_correct is not None:
            return
        try:
            wow_folder.default_config(self, GnomeDialog, self.wow_path)
            # TODO ПРОВЕРИТЬ ПРОФИЛЬ
            os.startfile(self.wow_path)
            self.wow_correct = True
            self.check_wow()
        except Exception as E:
            print(repr(E))

    def check_wow(self):
        def is_wow_launched():
            import psutil
            for proc in psutil.process_iter():
                if proc.name() == 'Wow.exe':
                    return True
            return False

        if self.GnomeDialog: #  Если необходима настройка скрипта
            self.ui.wow_text.setText('You must configure\nthe script before run WoW')
            self.ui.wow_text.setStyleSheet('color: red;')
            self.ui.start_wow.setCursor(QtGui.QCursor(QtCore.Qt.ForbiddenCursor))
            self.wow_correct = None
        else:
            wow_process = is_wow_launched()
            if wow_process and not self.wow_correct:
                self.ui.wow_text.setText('WoW launched incorrectly')
                self.ui.start_wow.setCursor(QtGui.QCursor(QtCore.Qt.ForbiddenCursor))
                self.ui.wow_text.setStyleSheet('color: red;')
                self.wow_correct = False
            elif wow_process:
                self.ui.wow_text.setText('WoW launched correctly')
                self.ui.start_wow.setCursor(QtGui.QCursor(QtCore.Qt.ForbiddenCursor))
                self.ui.wow_text.setStyleSheet('color: green;')
                self.wow_correct = True
            else:
                self.ui.wow_text.setText('WoW is not launched')
                self.ui.start_wow.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                self.ui.wow_text.setStyleSheet('color: blue;')
                self.wow_correct = None


    def event(self, event):  # Срабатывает при каждом вызове main.show()
        if event.type() == QtCore.QEvent.Show and not self.isHidden():
            self.wow_path = self.DB.query('SELECT data FROM system where variable="wow_path"')[0][0]
            self.spec = self.DB.query('SELECT data FROM system where variable="spec"')[0][0]
            self.class_= self.DB.query('SELECT data FROM system where variable="class"')[0][0]
            self.account_data = self.DB.query('SELECT data FROM system where variable in ("account", "server", "character")')

            if self.class_ is not None:
                self.ui.label.setPixmap(QtGui.QPixmap(resource_path(f'bin/img/main/{self.class_}.png')))
            if self.wow_path is None:
                if not self.GnomeDialog:
                    self.GnomeDialog = GnomeDialog(14, 'Hello, my Friend!\n\n'
                                                       'My name is Ho Linka and today i will help you to setup your routine.\n'
                                                       'First of all I need to know where your WoW client is.\n\n'
                                                       'Click "Settings"!')
                    self.GnomeDialog.show()
                    self.GnomeAwaits = self.settings.__name__
            elif not (self.account_data[1][0] or self.GnomeDialog):
                self.GnomeDialog = GnomeDialog(main=self, type='account', DB=self.DB, wow_path=self.wow_path)
                self.GnomeDialog.show()
            elif self.spec is None:
                if not self.GnomeDialog:
                    self.GnomeDialog = GnomeDialog(14, 'Now you need to choose your class and specialisation\n\n\n'
                                                       'Click "Class"!')
                    self.GnomeDialog.show()
                    self.GnomeAwaits = self.change_class.__name__
            elif self.spec is not None:
                binds = self.DB.query(f'SELECT * FROM {self.spec}')
                for bind in binds:
                    if bind[3] and bind[2] is None:
                        if not self.GnomeDialog:
                            self.GnomeDialog = GnomeDialog(14,
                                                           f'У тебя нет бинда на обязательной клавише: {bind[0]}\n\n'
                                                           'Click "Binds"!')
                        self.GnomeDialog.show()
                        self.GnomeAwaits = self.binds.__name__
                        break
            self.check_wow()
        return super(MainDialog, self).event(event)

    def binds(self):
        if self.GnomeDialog is not None and self.GnomeAwaits != self.binds.__name__:
            self.GnomeDialog.ui.bg.setPixmap(QtGui.QPixmap(resource_path("bin/img/gnome/nani.png")))
            return
        if not self.BindsDialog:
            self.BindsDialog = BindsDialog(self, self.spec)
            self.BindsDialog.show()

    def start(self):
        if self.GnomeDialog is not None and self.GnomeAwaits != self.start.__name__:
            self.GnomeDialog.ui.bg.setPixmap(QtGui.QPixmap(resource_path("bin/img/gnome/nani.png")))
            return
        # TODO Проверить \/
        elif self.GnomeDialog is None and not self.wow_correct:
            self.GnomeDialog = GnomeDialog(14, "\nYou can't run routine while WoW launched not with script"
                                               "or not launched at all\n\n"
                                               "You must launch WoW with 'Start WoW' button", True, self)
            self.GnomeDialog.show()
            return
        if not self.listener:
            ahk = ahk_console()
            wow = ahk.get_wow()
            if wow:
                self.ui.start.setIcon(self.stop_icon)
                self.listener = ahk.rotation_listener(wow, 'F1')
        else:
            self.ui.start.setIcon(self.start_icon)
            self.listener.stop()
            self.listener = None

    def settings(self):
        if self.GnomeDialog is not None and self.GnomeAwaits != self.settings.__name__:
            self.GnomeDialog.ui.bg.setPixmap(QtGui.QPixmap(resource_path("bin/img/gnome/nani.png")))
            return
        self.hide()
        if self.GnomeDialog is not None:
            self.GnomeDialog.close()
        self.SettingsDialog = SettingsDialog(self, self.account_data[1][0])
        self.SettingsDialog.show()

    def change_class(self):
        if self.GnomeDialog is not None and self.GnomeAwaits != self.change_class.__name__:
            self.GnomeDialog.ui.bg.setPixmap(QtGui.QPixmap(resource_path("bin/img/gnome/nani.png")))
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
        self.m_label = True

    def mouseReleaseEvent(self, event):
        self.m_label = False

    def mouseMoveEvent(self, event):
        if self.m_label:
            delta = QtCore.QPoint(event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()