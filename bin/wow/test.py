# from bin.wow.ahk_console import ahk_console
#
# def test():
#     spec = 'elemental'
#     ahk = ahk_console(spec)
#     wow = ahk.get_wow()
#     if wow:
#         with open('elemental.ahk', 'r', encoding='utf-8') as code_file:
#             script = code_file.read()
#         listener = ahk.rotation_listener(wow, script, 'e', '1', '0')
#         listener = ahk.rotation_listener(wow, script, 'q', '0', '0')

import os
from ahk import AHK
from ahk.window import Window
ahk = AHK(executable_path='C:\\Users\\Max\\Documents\\GitHub\\client_jbp\\bin\\wow\\drivers\\a64.exe')
print(ahk)
import psutil
for proc in psutil.process_iter():
    if proc.name() == 'Wow.exe':
        print(proc)
        print(proc.name())
        print(proc.pid)
        win = Window.from_pid(ahk, pid=proc.pid)
        print(win)

while True:
    pass
