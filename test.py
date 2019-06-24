from pathlib import Path, PureWindowsPath
import os


wow_path = 'H:/World of Warcraft/_retail_/Wow.exe'

wow_path = PureWindowsPath(os.path.dirname(os.path.abspath(wow_path)))
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
        lines = ([f'SET {k} {v}' for k, v in line_dict.items()])
        print(type(lines))
        print(lines)
        config_file = open(config_path, 'w', encoding='UTF-8')
        config_file.writelines(lines)
        config_file.close()
