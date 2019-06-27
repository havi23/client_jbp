from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSlot
from ui.gnome_be import GnomeDialog
from ui.main_window import Ui_Dialog as Ui_MainDialog
from ui.spec_be import ClassDialog
from ui.binds import Ui_Dialog as BindsDialog
from ui.settings import Ui_Dialog as Ui_SettingsDialog
import sys
from db_connect import Database
import time
from pathlib import Path, PureWindowsPath
import os
from ui.resource_to_exe import resource_path
DB = Database()

#  pyuic5 binds.ui -o binds.py





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
            self.GnomeDialog.ui.bg.setPixmap(QtGui.QPixmap(resource_path(f"ui/img/gnome/nani.png")))
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
        self.default_config(wow_path)
        # TODO Проверить аддон, загрузить, если его нет, настроить ТМВ, переписать конфиг


    def default_config(self, wow_path):
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
                #TODO Оконный режим
                lines = ([f'SET {k} {v}' for k, v in line_dict.items()])
                config_file = open(config_path, 'w', encoding='UTF-8')
                config_file.writelines(lines)
                config_file.close()
        else:
            if not self.GnomeDialog:
                self.GnomeDialog = GnomeDialog(14, 'Something going wrong!\n'
                                                   'I guess you must choose WoW directory again.\n\n'
                                                   'Click "Choose WoW directory"!')
                self.GnomeAwaits = self.cwp.__name__
            print('Не найден файл Config.wtf')
            return


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
        if event.type() == QtCore.QEvent.Show and not self.isHidden():
            self.GnomeDialog = None
            self.GnomeAwaits = None
            self.ClassDialog = None
            self.SettingsDialog = None
            self.BindsDialog = None
            self.wow_path = DB.query('SELECT data FROM system where variable="wow_path"')[0][0]
            self.spec = DB.query('SELECT data FROM system where variable="spec"')[0][0]
            self.class_= DB.query('SELECT data FROM system where variable="class"')[0][0]
            if self.class_ is not None:
                self.ui.label.setPixmap(QtGui.QPixmap(resource_path(f'ui/img/{self.class_}.png')))

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
        return super(MainDialog, self).event(event)

    def binds(self):
        if self.GnomeDialog is not None and self.GnomeAwaits != self.binds.__name__:
            self.GnomeDialog.ui.bg.setPixmap(QtGui.QPixmap(resource_path(f"ui/img/gnome/nani.png")))
            return
        if not self.BindsDialog:
            self.BindsDialog = BindsDialog(self, self.spec)
            #self.BindsDialog.show()

    def start(self):
        if self.GnomeDialog is not None and self.GnomeAwaits != self.start.__name__:
            self.GnomeDialog.ui.bg.setPixmap(QtGui.QPixmap(resource_path(f"ui/img/gnome/nani.png")))
            return
        pass

    def settings(self):
        if self.GnomeDialog is not None and self.GnomeAwaits != self.settings.__name__:
            self.GnomeDialog.ui.bg.setPixmap(QtGui.QPixmap(resource_path(f"ui/img/gnome/nani.png")))
            return
        self.hide()
        if self.GnomeDialog is not None:
            self.GnomeDialog.close()
        self.SettingsDialog = SettingsDialog(self)
        self.SettingsDialog.show()

    def change_class(self):
        if self.GnomeDialog is not None and self.GnomeAwaits != self.change_class.__name__:
            self.GnomeDialog.ui.bg.setPixmap(QtGui.QPixmap(resource_path(f"ui/img/gnome/nani.png")))
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
