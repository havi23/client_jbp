from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSlot
from ui.gnome_be import GnomeDialog
from ui.main_window import Ui_Dialog as Ui_MainDialog
from ui.spec_be import ClassDialog
from ui.binds import Ui_Dialog as BindsDialog
from ui.settings import Ui_Dialog as Ui_SettingsDialog
from ui.bug_report_BE import BugReportDialog
import sys
from db_connect import Database

import time
from pathlib import Path, PureWindowsPath
import os
from ui.resource_to_exe import resource_path


from ahk_console import ahk_console

DB = Database()
#  pyuic5 main_window.ui -o main_window.py
def default_config(window, wow_path):
    wow_path = PureWindowsPath(os.path.dirname(os.path.abspath(wow_path)))
    config_path = Path(wow_path) / 'WTF' / 'Config.wtf'
    old_config_path = Path(wow_path) / 'WTF' / 'Config.wtf.old'
    if config_path.exists():
        import shutil
        shutil.copy(config_path, old_config_path)
        with open(config_path, 'r', encoding='UTF-8') as config_file:
            lines = config_file.readlines()
            line_dict = dict()
            [line_dict.update({line.split(' ')[1]: line.split(' ')[2]}) for line in lines]
            line_dict.update({'Gamma': '"1"\n'})
            line_dict.update({'Brightness': '"50"\n'})
            line_dict.update({'Contrast': '"50"\n'})
            line_dict.update({'Contrast': '"50"\n'})
            line_dict.update({'colorblindSimulator': '"2"\n'})
            # TODO Оконный режим
            lines = ([f'SET {k} {v}' for k, v in line_dict.items()])
            config_file = open(config_path, 'w', encoding='UTF-8')
            config_file.writelines(lines)
            config_file.close()
    else:
        if not window.GnomeDialog:
            window.GnomeDialog = GnomeDialog(14, 'Something going wrong!\n'
                                                 'I guess you must choose WoW directory again.\n\n'
                                                 'Go Settings > Click "Choose WoW directory"!')
            window.GnomeDialog.show()
            window.GnomeAwaits = 'settings'
        print('Не найден файл Config.wtf')
        return

class SettingsDialog(QtWidgets.QDialog):
    def __init__(self, main, parent=None):
        super(SettingsDialog, self).__init__(parent)
        self.ui = Ui_SettingsDialog()
        self.oldPos = self.pos()
        self.ui.setupUi(self)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.GnomeDialog = None
        self.GnomeAwaits = None
        self.wow_path = DB.query('SELECT data FROM system where variable="wow_path"')[0][0]
        self.ui.cwp.clicked.connect(self.cwp)
        self.ui.save.clicked.connect(lambda: self.save(main))
        if self.wow_path is None:
            self.GnomeDialog = GnomeDialog(14, '\n\n\nClick "Choose WoW path"!')
            self.GnomeDialog.show()
            self.GnomeAwaits = self.cwp.__name__

    def save(self, main):
        if main is not None:
            main.show()
        self.close()

    def cwp(self):
        if self.GnomeDialog is not None and self.GnomeAwaits != self.cwp.__name__:
            self.GnomeDialog.ui.bg.setPixmap(QtGui.QPixmap("ui/img/gnome/nani.png"))
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
        default_config(self, wow_path)
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

class MainDialog(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainDialog, self).__init__()
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
        self.start_icon.addPixmap(QtGui.QPixmap("ui/img/start.bmp"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.stop_icon = QtGui.QIcon()
        self.stop_icon.addPixmap(QtGui.QPixmap("ui/img/stop.bmp"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.listener = None
        self.m_label = None
        self.info_active = None
        self.ui.info.clicked.connect(self.info_frame)


    def info_frame(self):
        if self.info_active:
            icon4 = QtGui.QIcon()
            icon4.addPixmap(QtGui.QPixmap("ui/img/info.bmp"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.info.setIcon(icon4)
            self.ui.label.setGeometry(QtCore.QRect(442, 255, 261, 461))
            '''
            self.ui.info.setIcon(icon4)
            self.ui.info_bg = QtWidgets.QLabel()
            self.ui.info_bg.setGeometry(QtCore.QRect(120, 22, 981, 831))
            self.ui.info_bg.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
            self.ui.info_bg.setText("")
            self.ui.info_bg.setPixmap(QtGui.QPixmap("ui/img/info.png"))
            self.ui.info_bg.setObjectName("bg")
            '''
            if self.class_ is not None:
                self.ui.label.setPixmap(QtGui.QPixmap(f'ui/img/{self.class_}.png'))
            else:
                self.ui.label.setPixmap(QtGui.QPixmap(f'ui/img/noclass.png'))
            self.info_active = False
        else:
            icon4 = QtGui.QIcon()
            icon4.addPixmap(QtGui.QPixmap("ui/img/info_c.bmp"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.info.setIcon(icon4)
            self.ui.label.setGeometry(QtCore.QRect(121, 7, 1021, 861))
            self.ui.label.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
            self.ui.label.setText("")
            self.ui.label.setPixmap(QtGui.QPixmap(resource_path("ui\\img\\info_bg.png")))
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
            default_config(self, self.wow_path)
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
            self.GnomeDialog = None
            self.GnomeAwaits = None
            self.ClassDialog = None
            self.SettingsDialog = None
            self.BindsDialog = None
            self.BugReport = None
            self.wow_path = DB.query('SELECT data FROM system where variable="wow_path"')[0][0]
            self.spec = DB.query('SELECT data FROM system where variable="spec"')[0][0]
            self.class_= DB.query('SELECT data FROM system where variable="class"')[0][0]

            if self.class_ is not None:
                self.ui.label.setPixmap(QtGui.QPixmap(f'ui/img/{self.class_}.png'))
            if self.wow_path is None:
                if not self.GnomeDialog:
                    self.GnomeDialog = GnomeDialog(14, 'Hello, my Friend!\n\n'
                                                       'My name is Ho Linka and today i will help you to setup your routine.\n'
                                                       'First of all I need to know where your WoW client is.\n\n'
                                                       'Click "Settings"!')
                self.GnomeDialog.show()
                self.GnomeAwaits = self.settings.__name__

            elif self.spec is None:
                if not self.GnomeDialog:
                    self.GnomeDialog = GnomeDialog(14, 'Now you need to choose your class and specialisation\n\n\n'
                                                       'Click "Class"!')
                    self.GnomeDialog.show()
                    self.GnomeAwaits = self.change_class.__name__
            elif self.spec is not None:
                binds = DB.query(f'SELECT * FROM {self.spec}')
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
            self.GnomeDialog.ui.bg.setPixmap(QtGui.QPixmap("ui/img/gnome/nani.png"))
            return
        if not self.BindsDialog:
            self.BindsDialog = BindsDialog(self, self.spec)
            self.BindsDialog.show()

    def start(self):
        if self.GnomeDialog is not None and self.GnomeAwaits != self.start.__name__:
            self.GnomeDialog.ui.bg.setPixmap(QtGui.QPixmap("ui/img/gnome/nani.png"))
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
        print(self.settings.__name__)
        if self.GnomeDialog is not None and self.GnomeAwaits != self.settings.__name__:
            self.GnomeDialog.ui.bg.setPixmap(QtGui.QPixmap("ui/img/gnome/nani.png"))
            return
        self.hide()
        if self.GnomeDialog is not None:
            self.GnomeDialog.close()
        self.SettingsDialog = SettingsDialog(self)
        self.SettingsDialog.show()

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
        self.m_label = True

    def mouseReleaseEvent(self, event):
        self.m_label = False

    def mouseMoveEvent(self, event):
        if self.m_label:
            delta = QtCore.QPoint(event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()
