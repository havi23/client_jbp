#pyuic5 gnome.ui -o gnome.py

from ahk import AHK, Hotkey
from ahk.window import Window
from db_connect import Database
import psutil
DB = Database()


def ahk_start():
    try:
        ahk = AHK(executable_path='C:\\Users\Max\\PycharmProjects\\client_jbp\\drivers\\a64.exe')
        for proc in psutil.process_iter():
            if proc.name() == 'a64.exe':
                ahk_pid = proc.pid
                break
        return ahk
    except:
        print('Ошибка загрузки модуля AY')
        exit()

def get_wow(ahk):
    for proc in psutil.process_iter():
        if proc.name() == 'Wow.exe':
            wow = Window.from_pid(ahk, pid=proc.pid)
            return wow
    print('Не найден WoW')
    return 0

def rotation(ahk, wow, dmg_):
    spell, color, bind = DB.query('SELECT * FROM sub')[0]
    print(spell, color, bind)
    script = \
        f'''
        #NoTrayIcon
        ControlSend,, {bind}, ahk_id {wow.id};
        '''
    hk = Hotkey(ahk, dmg_, script)
    hk.start()  # listener process activated
    return hk


def stop(hk):
    try:
        hk.stop()
        return True
    except:
        return False

if __name__ == '__main__':
    ahk = ahk_start()
    wow = get_wow(ahk)
    if wow != 0:
        run_hk = rotation(ahk, wow, 'e')
        while True:
            pass
        #stop(run_hk)








