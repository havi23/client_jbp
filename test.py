def get_content(path, character_name, server):
    with open(f'{path}\\TellMeWhen1.lua', 'r', encoding='utf-8') as tmw_config:
        tmw_config = tmw_config.read()
        if 'TellMeWhenDB' in tmw_config:
            # Эта строка в файле встречается дважды. ИМЯПЕРСОНАЖА - СЕРВЕР.
            character_string = f'{character_name} - {server}'
            # Если есть конфиг на персонажа
            if character_string in tmw_config:  # Old config was found
                profile_name = tmw_config.split(f'["{character_name} - {server}"] = "')[1].split(',')[0][:-1]
                print(profile_name)
                profile = tmw_config.split(f'["{profile_name}"] = {{')[1]
                profile = profile.split('\n\t\t},')[0]
                return profile
            else:  # This is first run
                pass

def generate_config():
    with open('C:\\Users\\Max\\Documents\\0 Дела\\jbp\\Генератор TMW\\tmw_file.lua', 'w', encoding='utf-8') as new_file:
        character_name = 'Петрпустота'
        server = 'Страж Смерти'
        path = 'C:\\Users\\Max\\Documents\\0 Дела\\jbp\\Генератор TMW\\'
        content = get_content(path, character_name, server)
        new_file.write(content)

def replace(character_name, server, path_from, path_to):
    with open(f'{path_from}', 'r', encoding='utf-8') as new_profile:
        new_profile = new_profile.read()
    with open(f'{path_to}\\TellMeWhen1.lua', 'r', encoding='utf-8') as content:
        content = content.read()
    old_profile = get_content(path_to, character_name, server)
    with open(f'{path_to}\\TellMeWhen1.lua', 'w', encoding='utf-8') as new_file:
        print(old_profile)
        new_file.write(content.replace(old_profile, new_profile))

character_name = 'Тестовыйф'
server = 'Страж Смерти'
path_from = 'C:\\Users\\Max\\Documents\\0 Дела\\jbp\\Генератор TMW\\profile.lua'
path_to = 'C:\\Users\\Max\\Documents\\0 Дела\\jbp\\Генератор TMW'
replace(character_name, server, path_from, path_to)
