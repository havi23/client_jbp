from db_connect import Database
import csv
DB = Database()

with open('spell_dict.csv', 'r', encoding='utf-8') as csv_file:
    rows = csv.reader(csv_file)
    spell_names = []
    for row in rows:
        if row == []:
            continue
        row = row[0].split(';')
        class_, spec_list, spell_id, spell_name = row[0], row[1].split('+'), row[2], row[3]
        print(spell_name)
        if spell_name in spell_names:
            continue
        spell_names.append(spell_name)
        if spec_list[0] == 'all':
            spec_list = DB.query(f'select * from specs where lower(class)="{class_}"')
            spec_list = spec_list[0][1:4]
        specs_done = []
        for spec in spec_list:
            if spec in specs_done:
                continue
            specs_done.append(spec)
            if spec is None:
                continue
            try:
                DB.execute(f'INSERT INTO {spec} VALUES ("{spell_name}", Null, 1);')
            except Exception as E:
                if 'UNIQUE' not in str(E):
                    query = 'INSERT INTO {} VALUES '.format(f'{spec}_{class_}') +\
                            f'("{spell_name}", Null, 1);'
                    DB.execute(query)
                else:
                    print(E)
                    print(spell_name, spell_id, spec)
    DB.commit()
