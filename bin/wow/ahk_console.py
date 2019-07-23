from ahk import AHK, Hotkey
from ahk.window import Window
from db_connect import Database
import psutil
DB = Database()


class ahk_console():
    def __init__(self):
        try:
            self.ahk = AHK(executable_path=f"bin/wow/drivers/a64.exe")
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
                return Window.from_pid(self.ahk, pid=proc.pid)
        print('Не найден WoW')
        return False

    def rotation_listener(self, wow, dmg_):
        #spell, color, bind = DB.query('SELECT * FROM sub')[0]
        #print(spell, color, bind)
        bind = 'TEST'
        script = \
            f'''
            #NoTrayIcon
            ControlSend,, {bind}, ahk_id {wow.id};
            '''
        hk = Hotkey(self.ahk, dmg_, script)
        hk.start()  # listener process activated
        return hk


if __name__ == '__main__':
    ahk = ahk_console()
    wow = ahk.get_wow()
    if wow:
        listener = ahk.rotation_listener(wow, 'F1')


    while True:
        pass









