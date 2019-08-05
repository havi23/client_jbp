from bin.Qt.license_key_Qt import Ui_Dialog as Ui_LicenseKeyDialog
from PyQt5 import QtWidgets, QtCore
from server import Server, internet_on
from db_connect import Database
from bin.main_window import MainDialog

#  pyuic5 license_key.ui -o license_key_Qt.py

class LicenseKeyDialog(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(LicenseKeyDialog, self).__init__(parent)
        from db_connect import Database
        self.DB = Database()
        # self.oldPos = self.pos()
        self.ui = Ui_LicenseKeyDialog()
        self.ui.setupUi(self)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool)
        self.ui.submit.mousePressEvent = lambda event: self.submit()
        self.ui.website.mousePressEvent = lambda event: self.website()
        self.ui.exit_.mousePressEvent = lambda event: self.exit_()
        self.ui.error.setText("WARNING: A computer will be attached to the key. "
                              "The key you entered will not work on another PC")
        self.ui.key_edit.setPlaceholderText("Enter a license key")


    def submit(self):
        key = self.ui.key_edit.text()
        server = Server()
        status = server.connect(key)
        if status == 'token':
            self.ui.error.setText("This key is not exists or has been activated early on another PC.\n"
                                  "Go to website for support.")
            self.ui.key_edit.setPlaceholderText('Enter a license key')
        elif status == 'server':
            if internet_on:
                self.ui.error.setText("We have a problems with our server now. Try again later.")
                self.ui.key_edit.setPlaceholderText('Sorry ):')
            else:
                self.ui.error.setText("Check your internet connection")
        else:
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
