from bin.Qt.license_key_Qt import Ui_Dialog as Ui_LicenseKeyDialog
from PyQt5 import QtWidgets, QtCore, QtGui
from server import Server, internet_on
from db_connect import Database
from bin.main_window import MainDialog
from bin.resource_to_exe import resource_path

#  pyuic5 license_key.ui -o license_key_Qt.py

class LicenseKeyDialog(QtWidgets.QMainWindow):
    def __init__(self, parent=None, error_code=None):
        super(LicenseKeyDialog, self).__init__(parent)
        from db_connect import Database
        self.DB = Database()
        # self.oldPos = self.pos()
        self.ui = Ui_LicenseKeyDialog()
        self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(resource_path('bin\\img\\key.png')))
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # self.setAttribute(QtCore.Qt.WA_NoSystemBackground | QtCore.Qt.WA_TranslucentBackground)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.ui.submit.mousePressEvent = lambda event: self.submit()
        self.ui.website.mousePressEvent = lambda event: self.website()
        self.ui.exit_.mousePressEvent = lambda event: self.exit_()
        self.error_dictionary = {
            'server': 'Check your internet connection' if not internet_on()
            else 'We have a problems with our server now. Try again later.',
            'token': 'This key is not exists or has been activated early on another PC.\n" \
                                          "Go to website for support.',
            'key': 'Your key is incorrect.\nTry again or contact support',
            'hwid': 'This key has beed attached to another PC. Your cant use it',
            'date': 'Your subscribtion has ended.\nUpdate your key on JustBecome.PRO',
            'params': 'Unknown error. \nPlease contact support.',
            None: 'WARNING: A computer will be attached to the key. '
                  'The key you entered will not work on another PC'
            }
        self.ui.error.setText(self.error_dictionary[error_code])
        self.ui.key_edit.setPlaceholderText("Enter a license key")

    def submit(self):
        key = self.ui.key_edit.text()
        server = Server()
        error_code = server.connect(key)
        self.ui.error.setText(self.error_dictionary[error_code])
        if not error_code:
            DB = Database()
            DB.execute('UPDATE system SET data=? WHERE variable="license_key"', (key,))
            DB.commit()
            main = MainDialog(server, self)
            main.show()

    def exit_(self):
        exit()

    def website(self):
        print('GO TO SITE')

    # def mousePressEvent(self, event):
    #     self.oldPos = event.globalPos()
    #
    # def mouseMoveEvent(self, event):
    #     delta = QtCore.QPoint(event.globalPos() - self.oldPos)
    #     self.move(self.x() + delta.x(), self.y() + delta.y())
    #     self.oldPos = event.globalPos()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            event.ignore()
        elif event.key() == QtCore.Qt.Key_Enter:
            pass

    def run_UI(self, server):
        app = QtWidgets.QApplication([])
        main = MainDialog(server)
        main.show()
        sys.exit(app.exec())
