#!/usr/bin/python3
from ahk import AHK, Hotkey
from ahk.window import Window
import psutil


def get_wow():
    for proc in psutil.process_iter():
        if proc.name() == 'Wow.exe':
            wow = Window.from_pid(ahk, pid=proc.pid)
            return wow
    print('Не найден WoW')
    return 0


try:
    ahk = AHK(executable_path='C:\\Users\Max\\PycharmProjects\\client_jbp\\drivers\\a64.exe')
    for proc in psutil.process_iter():
        if proc.name() == 'a64.exe':
            ahk_pid = proc.pid
            break
except:
    print('Ошибка загрузки модуля AY')
    exit()

wow = get_wow()
if not wow:
    exit()
# win = ahk.win_get(title='World of Warcraft')
print(wow.id)

ahk_init = '''
I_Icon = C:\\test.ico
IfExist, %I_Icon%
  Menu, Tray, Icon, %I_Icon%, 1, 1;
'''
ahk.run_script(ahk_init, blocking=False)

binds = {'ambush': 'q'}
script = f'''
#NoTrayIcon
ControlSend,, {binds['ambush']}, ahk_id {wow.id};
'''
hotkey = Hotkey(ahk, 'F1', script)
hotkey.start()  # listener process activated

while True:
    pass

# win.send('hi')
# win = Window(ahk, ahk_id='0x1e0bc0')  # by ahk_id
# print(win)