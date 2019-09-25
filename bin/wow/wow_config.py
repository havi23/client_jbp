from pathlib import Path, PureWindowsPath
from bin.gnome import GnomeDialog
import os, shutil
from bin.resource_to_exe import resource_path

def default_config(main, GnomeDialog, wow_path):
    wow_path = PureWindowsPath(os.path.dirname(os.path.abspath(wow_path)))
    print(wow_path)
    addon_path = Path(f'{wow_path}\\Interface\\AddOns')
    account_data = main.account_data
    account_path = Path(f'{wow_path}\\WTF\\Account\\{account_data[0][0]}\\SavedVariables')
    print(account_path)
    config_path = Path(f'{wow_path}\\WTF\\Config.wtf')
    old_config_path = Path(f'{wow_path}\\WTF\\Config.wtf.old')
    if config_path.exists() and account_path.exists():
        shutil.copy(config_path, old_config_path)
        with open(config_path, 'r', encoding='UTF-8') as config_file:
            lines = config_file.readlines()
            line_dict = dict()
            [line_dict.update({line.split(' ')[1]: line.split(' ')[2]}) for line in lines]
            line_dict.update({'Gamma': '"1"\n'})
            line_dict.update({'Brightness': '"50"\n'})
            line_dict.update({'Contrast': '"50"\n'})
            line_dict.update({'colorblindSimulator': '"0"\n'})
            # TODO Оконный режим
            lines = ([f'SET {k} {v}' for k, v in line_dict.items()])
            config_file = open(config_path, 'w', encoding='UTF-8')
            config_file.writelines(lines)
            config_file.close()
        with open(f'{account_path}\\JustBecomePro.lua', 'w', encoding='utf-8') as profile_file:
            profile_file.write(main.profile)
    else:
        if not main.GnomeDialog:
            main.GnomeDialog = GnomeDialog(14, 'Something going wrong!\n'
                                                 'I guess you must choose WoW directory again.\n\n'
                                                 'Go Settings > Click "Choose WoW directory"!')
            main.GnomeDialog.show()
            main.GnomeAwaits = 'settings'
        print('Не найден файл Config.wtf')
        return
    print(account_data)  # [('102603599#1',), ('Баклажановая',), ('Гордунни',)]
    print(addon_path)  # G:\World of Warcraft\_retail_\Interface\Addons
    from_addon_path = resource_path('bin\\wow\\addon\\')
    files = os.listdir(from_addon_path)
    files.sort()
    for f in files:
        src = os.path.join(from_addon_path, f)
        dst = os.path.join(addon_path, f)
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst)

