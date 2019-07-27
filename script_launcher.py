'''
Запрос "AUTH" на сервер (версия, ключ)
    Если версия программы устарела:
        Вернуть ошибку "Некорректная версия программы"
    Если ключ корректный:
        Вернуть оплаченные на ключе классы+спеки (в XML, наверное)
    Если ключ некорректный:
        Вернуть ошибку "Ключ не найден"

Запрос "GET_COLORS" (ключ, класс, спек)
    Если на ключе активен класс, спек:
        Вернуть <chip_shot>"X"</chip_shot) -- соответствие цветов и абилок
'''
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
    app = QtWidgets.QApplication([])
    if not key:
        key = DB.query('SELECT data FROM system WHERE variable="license_key"')[0][0]
        print(key)
    if key:
        server = Server()
        connected = server.connect(key)
        update_check(server)
        if not connected:
            DB.execute('UPDATE system SET data=? WHERE variable="license_key"', (None,))
            DB.commit()
            auth()
        else:
            run_UI(server)
    else:
        from bin.license_key import LicenseKeyDialog
        KeyDialog = LicenseKeyDialog()
        KeyDialog.show()
        sys.exit(app.exec())

if __name__ == '__main__':
    auth()