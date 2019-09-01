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

def auth(key=None, error_message=None):
    if not key:
        key = DB.query('SELECT data FROM system WHERE variable="license_key"')[0][0]
    if key:
        server = Server()
        error_code = server.connect(key)
        print(error_code)
        #if error_code in ('server', 'token', 'key', 'hwid', 'date', 'params'):
        if not error_code:
            # TODO if 'server' - сделать уведомление. + сделать msgbox
            DB.execute('UPDATE system SET data=? WHERE variable="license_key"', (None,))
            DB.commit()
            auth(error_code=error_code)
        update_check(server)
        run_UI(server)
    else:
        from bin.license_key import LicenseKeyDialog
        app = QtWidgets.QApplication([])
        KeyDialog = LicenseKeyDialog(error_message=error_message)
        KeyDialog.show()
        sys.exit(app.exec())

if __name__ == '__main__' and 1==0:
    DB = Database()
    def restarter(last_error=None):
        try:
            auth()
        except Exception as E:
            error = repr(E)
            # Если ошибка повторяется
            if error == last_error:
                DB.execute(f'INSERT INTO error_log VALUES (CURRENT_TIMESTAMP, "SECOND: {error}")')
                DB.commit()
                return
            DB.execute(f'INSERT INTO error_log VALUES (CURRENT_TIMESTAMP, "{error}")')
            DB.commit()
            restarter(error)
    restarter()
else:
    auth()
