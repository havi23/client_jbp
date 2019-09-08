from pathlib import Path, PureWindowsPath
from bin.gnome import GnomeDialog
import os


def default_config(main, GnomeDialog, wow_path):
    wow_path = PureWindowsPath(os.path.dirname(os.path.abspath(wow_path)))
    addon_path = Path(wow_path) / 'Interface' / 'Addons'
    account_data = main.account_data
    print(account_data) #  [('102603599#1',), ('Баклажановая',), ('Гордунни',)]
    print(addon_path) #  G:\World of Warcraft\_retail_\Interface\Addons
    return
    config_path = Path(wow_path) / 'WTF' / 'Config.wtf'
    old_config_path = Path(wow_path) / 'WTF' / 'Config.wtf.old'
    if config_path.exists():
        import shutil
        shutil.copy(config_path, old_config_path)
        with open(config_path, 'r', encoding='UTF-8') as config_file:
            lines = config_file.readlines()
            line_dict = dict()
            [line_dict.update({line.split(' ')[1]: line.split(' ')[2]}) for line in lines]
            line_dict.update({'Gamma': '"1"\n'})
            line_dict.update({'Brightness': '"50"\n'})
            line_dict.update({'Contrast': '"50"\n'})
            line_dict.update({'Contrast': '"50"\n'})
            line_dict.update({'colorblindSimulator': '"2"\n'})
            # TODO Оконный режим
            lines = ([f'SET {k} {v}' for k, v in line_dict.items()])
            config_file = open(config_path, 'w', encoding='UTF-8')
            config_file.writelines(lines)
            config_file.close()
    else:
        if not main.GnomeDialog:
            main.GnomeDialog = GnomeDialog(14, 'Something going wrong!\n'
                                                 'I guess you must choose WoW directory again.\n\n'
                                                 'Go Settings > Click "Choose WoW directory"!')
            main.GnomeDialog.show()
            main.GnomeAwaits = 'settings'
        print('Не найден файл Config.wtf')
        return