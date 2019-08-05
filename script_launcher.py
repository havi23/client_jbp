from db_connect import Database
from server import Server
import sys
from PyQt5 import QtWidgets
import ctypes

DB = Database()
local_version = float(DB.query('select data from system where variable="version"')[0][0])


def run_UI(server):
    from bin.main_window import MainDialog
    import PyQt5
    app = PyQt5.QtWidgets.QApplication([])
    main = MainDialog(server)
    main.show()
    sys.exit(app.exec())

def update_check(server):
    update = server.check_update()
    if update:
        global_version = float(update)
        if local_version < global_version:
            print('running updater')
            server.load_updater()
            ctypes.windll.user32.MessageBoxW(0, "You must run update.exe before starting", "Update required", 0)
            sys.exit()
def auth(key=None):
    if not key:
        key = DB.query('SELECT data FROM system WHERE variable="license_key"')[0][0]
        print(key)
    if key:
        server = Server()
        status = server.connect(key)
        update_check(server)
        if status in ('server', 'token'):
            # TODO if 'server' - сделать уведомление. + сделать msgbox
            DB.execute('UPDATE system SET data=? WHERE variable="license_key"', (None,))
            DB.commit()
            auth()
        else:
            run_UI(server)
    else:
        from bin.license_key import LicenseKeyDialog
        app = QtWidgets.QApplication([])
        KeyDialog = LicenseKeyDialog()
        KeyDialog.show()
        sys.exit(app.exec())

if __name__ == '__main__':
    auth()