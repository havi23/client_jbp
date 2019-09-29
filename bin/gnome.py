from PyQt5 import QtWidgets, QtCore, QtGui
from bin.Qt.gnome_Qt import Ui_Dialog as Ui_GnomeDialog
import os

class GnomeDialog(QtWidgets.QDialog):
    # clicked = QtCore.pyqtSignal(str)
    def __init__(self, size=16, text='', button=None, main=None, _type=None, DB=None, wow_path=None, parent=None,
                 settings=None):
        super(GnomeDialog, self).__init__(parent)
        self.ui = Ui_GnomeDialog()
        self.ui.setupUi(self)
        self.main = main
        self.settings = settings
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
        if _type == 'account':
            self.ui.okay.clicked.connect(lambda: self.save(main, DB))
            self.setAccount(wow_path)
        elif button:
            self.ui.okay.clicked.connect(lambda: self._close(main))
        else:
            self.ui.okay.hide()

    def setAccount(self, wow_path):
        # TODO Сделать рекурсивной
        self.ui.text.setText('\n\nSelect your character')
        self.account_edit = QtWidgets.QComboBox(self)
        self.account_edit.setGeometry(234, 287, 109, 25)
        self.server_edit = QtWidgets.QComboBox(self)
        self.server_edit.setGeometry(341, 287, 109, 25)
        self.character_edit = QtWidgets.QComboBox(self)
        self.character_edit.setGeometry(448, 287, 109, 25)
        self.account_edit.currentTextChanged.connect(lambda: self.setServer(wow_path))
        self.server_edit.currentTextChanged.connect(lambda: self.setCharacter(wow_path))
        try:
            account_list = next(os.walk(wow_path.split('_retail_')[0].replace('/', '\\') + '_retail_\\WTF\\Account'))[1]
            if any('#' in account for account in account_list):
                if 'SavedVariables' in account_list: account_list.remove('SavedVariables')
                self.account_edit.addItems(account_list)
                self.account_edit.update()
                self.setServer(wow_path)
                self.setCharacter(wow_path)
        except Exception as E:
            self.ui.text.setText('\nYou must login to character at least once before start script.\n\n'
                                 'Do it and restart this program')
            self.account_edit.close()
            self.server_edit.close()
            self.character_edit.close()
            self.ui.okay.clicked.connect(lambda: self._close(self.main))
            print(repr(E))
            return

    def setServer(self, wow_path):
        self.account_edit.update()
        #print(self.account_edit.currentText())
        server_list = next(os.walk(wow_path.split('_retail_')[0].replace('/', '\\') +
                                   '_retail_\\WTF\\Account\\'
                                   f'{self.account_edit.currentText()}\\'))[1]
        if 'SavedVariables' in server_list: server_list.remove('SavedVariables')
        self.server_edit.clear()
        self.server_edit.addItems(server_list)
        self.server_edit.update()

    # def event(self, event):
    #     if event.type() == QtCore.QEvent.Close:
    #         self.main.GnomeDialog = None
    #         return True
    #     else:
    #         return False

    def setCharacter(self, wow_path):
        character_list = next(os.walk(wow_path.split('_retail_')[0].replace('/', '\\') +
                                   '_retail_\\WTF\\Account\\'
                                   f'{self.account_edit.currentText()}\\'
                                   f'{self.server_edit.currentText()}\\'))[1]
        if 'SavedVariables' in character_list: character_list.remove('SavedVariables')
        self.character_edit.clear()
        self.character_edit.addItems(character_list)
        self.character_edit.update()


    def save(self, main, DB):
        nickname = self.character_edit.currentText()
        DB.execute(f'UPDATE system SET data="{self.account_edit.currentText()}" WHERE variable="account"')
        DB.execute(f'UPDATE system SET data="{self.server_edit.currentText()}" WHERE variable="server"')
        DB.execute(f'UPDATE system SET data="{nickname}" WHERE variable="character"')
        DB.commit()
        try:
            main.ui.character_change() # TODO Проверить 05.08
            main.ui.character_label.setText(self.character_edit.currentText())
        except:
            main.account_data = DB.query('SELECT data FROM system where variable in ("account", "server", "character")')
        if self.settings:
            self.settings.ui.character_label.setText(nickname)
        self._close(main)

    def _close(self, main):
        # if main:
        #     if main.GnomeDialog:
        #         main.GnomeDialog = None
        self.main.GnomeDialog = None
        self.close()

