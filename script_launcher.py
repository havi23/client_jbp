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

def auth(key=None, error_code=None):
    if not key:
        key = DB.query('SELECT data FROM system WHERE variable="license_key"')[0][0]
        try:
            if key:
                server = Server()
                error_code = server.connect(key)
                print(f'>{error_code}')
                if error_code in ('server', 'token', 'key', 'hwid', 'date', 'params'):
                # if not error_code:
                    DB.execute('UPDATE system SET data=? WHERE variable="license_key"', (None,))
                    DB.commit()
                    auth(error_code=error_code)
                # else:
                #     error_code = 'key'
                #     raise Exception
                update_check(server)
                run_UI(server)
            else:
                raise Exception
        except Exception as E:
            print(f'script_launcher.auth EXCEPTION: {repr(E)}')
            from bin.license_key import LicenseKeyDialog
            app = QtWidgets.QApplication([])
            KeyDialog = LicenseKeyDialog(error_code=error_code)
            KeyDialog.show()
            sys.exit(app.exec())

if __name__ == 'main' and 1!=0:
    DB = Database()
    def restarter(last_error=None):
        try:
            auth()
        except Exception as E:
            error = repr(E)
            print(error)
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

