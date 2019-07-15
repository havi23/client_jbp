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
import sys

# TODO В разработке
DB = Database()
server_version = 0.0 #  POST-запрос, отдать ключ, получить версию программы
local_version = float(DB.query('select data.db from system where variable="version"')[0][0])

def run_UI():
    from ui.ui import MainDialog
    from PyQt5 import QtWidgets
    app = QtWidgets.QApplication([])
    main = MainDialog()
    main.show()
    sys.exit(app.exec())

if server_version > local_version:
    print('update')

elif server_version == local_version:
    run_UI()
else:
    if __name__ == '__main__':
        print('dev version started ')
        run_UI()


