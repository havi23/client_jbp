from ahk import AHK, Hotkey
from ahk.window import Window
from db_connect import Database
from bin.resource_to_exe import resource_path
import os
import psutil

DB = Database()

class ahk_console():
    def __init__(self):
        try:
            path = os.path.join("drivers", "a64.exe")
            #path = 'C:\\Users\\Max\\Documents\\GitHub\\client_jbp\\bin\\wow\\drivers\\a64.exe'
            #path = resource_path('bin\\wow\\drivers\\a64.exe')
            self.ahk = AHK(executable_path=path)
            print(path)
            for proc in psutil.process_iter():
                if proc.name() == 'a64.exe':
                    self.ahk_pid = proc.pid
                    break
        except Exception as E:
            print('Ошибка загрузки модуля AY')
            print(repr(E))

    def get_wow(self):
        for proc in psutil.process_iter():
            if proc.name() == 'Wow.exe':
                print(proc)
                print(proc.name())
                print(proc.pid)
                return Window.from_pid(self.ahk, pid=proc.pid)
        print('Не найден WoW')
        return False

    def rotation_listener(self, wow, dmg_key, color, bind, x, y):
        # spell, color, bind = DB.query('SELECT * FROM sub')[0]
        # print(spell, color, bind)
        # bind = 'TEST'
        # script = \
        #     f'''
        #     #NoTrayIcon
        #     ControlSend,, {bind}, ahk_id {wow.id};
        #     '''
        script = \
            f'PixelGetColor,Color,{x},{y};' \
                f'If Color=0x{color}' \
                '{' \
                f'ControlSend,, {bind}, ahk_id {wow.id};' \
                '}'
        print(script)
        hk = Hotkey(self.ahk, dmg_key, script)
        hk.start()  # listener process activated
        return hk


if __name__ == '__main__':
    ahk = ahk_console()
    wow = ahk.get_wow()
    if wow:
        listener = ahk.rotation_listener(wow, 'F1', '775B5B', '3', '17', '26')

    while True:
        pass
