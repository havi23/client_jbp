from db_connect import Database
from ahk import AHK, Hotkey
from ahk.window import Window

DB = Database()
print(DB.query('SELECT * FROM abilitys'))


while True:
    pass


