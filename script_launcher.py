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

DB = Database()
server_version = 1.0 #  POST-запрос, отдать ключ, получить версию программы
local_version = float(DB.query('select data from system where variable="version"')[0][0])
url = 'http://127.0.0.1:8000/'

def run_UI(server):
    from bin.main_window import MainDialog
    import PyQt5
    app = PyQt5.QtWidgets.QApplication([])
    main = MainDialog(server)
    main.show()
    sys.exit(app.exec())

def hwid_generate():
    import uuid
    return uuid.UUID(int=uuid.getnode())

if server_version > local_version:
    print('update')

elif server_version == local_version:
    #  TODO Если нет key - запросить.
    from PyQt5 import QtWidgets
    from bin.license_key import LicenseKeyDialog
    app = QtWidgets.QApplication([])
    LicenseKeyDialog = LicenseKeyDialog(url)
    LicenseKeyDialog.show()
    sys.exit(app.exec())
else:
    print('dev version started ')
    url = 'http://127.0.0.1:8000/'
    key = '0300d200b078e4d1a4f522536220d133'
    hwid = hwid_generate()
    server = Server()
    status = server.connect(url, key, hwid)
    if status:
        run_UI(server)


