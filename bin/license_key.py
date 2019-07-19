from bin.Qt.license_key_Qt import Ui_Dialog as Ui_LicenseKeyDialog
from PyQt5 import QtWidgets, QtCore
from server import Server

class LicenseKeyDialog(QtWidgets.QMainWindow):
    def __init__(self, url, parent=None):
        super(LicenseKeyDialog, self).__init__(parent)
        from db_connect import Database
        self.DB = Database()
        self.url = url
        self.oldPos = self.pos()
        self.ui = Ui_LicenseKeyDialog()
        self.ui.setupUi(self)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool)
        self.ui.submit.mousePressEvent = lambda event: self.submit()
        self.ui.website.mousePressEvent = lambda event: self.website()
        self.ui.exit_.mousePressEvent = lambda event: self.exit_()
        self.ui.error.setText("")


    def submit(self):
        key = self.ui.key_edit.text()
        import uuid
        hwid = str(uuid.UUID(int=uuid.getnode()))
        print(hwid)
        server = Server()
        status = server.connect(self.url, key, hwid)
        if not status:
            self.ui.error.setText("wrong key")
            self.ui.key_edit.setText('')
        else:
            from bin.main_window import MainDialog
            MainDialog = MainDialog(server, self)
            MainDialog.show()

    def exit_(self):
        exit()

    def website(self):
        print('GO TO SITE')

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
            pass

    def run_UI(self, server):
        from bin.main_window import MainDialog
        app = QtWidgets.QApplication([])
        main = MainDialog(server)
        main.show()
        sys.exit(app.exec())
