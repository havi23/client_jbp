from ahk import AHK, Hotkey
from ahk.window import Window
from db_connect import Database
from bin.resource_to_exe import resource_path
import os
import psutil


class ahk_console():
    def __init__(self, spec):
        self.spec = spec
        self.DB = Database()
        try:
            path = resource_path(os.path.join("bin", "wow", "drivers", "a64.exe"))
            #print(path)
            os.environ['AHK_PATH'] = path
            self.ahk = AHK()#executable_path=path)
            print(self.ahk)
            for proc in psutil.process_iter():
                if proc.name() == 'a64.exe':
                    self.ahk_pid = proc.pid
                    print(self.ahk_pid)
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
                win = Window.from_pid(self.ahk, pid=proc.pid)
                print(win)
                return win
        print('Не найден WoW')
        return False

    def rotation_listener(self, wow, script, dmg_key, x, y):
        binds = self.DB.query(f'SELECT * FROM {self.spec}')
        script = script.split('If')
        f_script = []
        for spell_name, bind, _ in binds:
            for block in script:
                if spell_name in block and bind is not None:
                    f_script.append(block.replace(spell_name, '{'+str(bind)+'}'))

        script = \
            f'ShowColor:\nPixelGetColor,Color,{x},{y}\n' \
                f'If{"If".join(f_script)}'
        script = script.replace('wow_id', wow.id)
        hk = Hotkey(self.ahk, dmg_key, script)
        hk.start()  # listener process activated
        return hk


if __name__ == '__main__':
    spec = 'elemental'
    ahk = ahk_console(spec)
    wow = ahk.get_wow()
    if wow:
        with open('elemental.ahk', 'r', encoding='utf-8') as code_file:
            script = code_file.read()
        listener = ahk.rotation_listener(wow, script, 'e', '1', '0')
        listener = ahk.rotation_listener(wow, script, 'q', '0', '0')

    while True:
        pass
