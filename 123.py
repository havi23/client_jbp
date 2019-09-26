from db_connect import Database
import csv
DB = Database()
with open('spell_dict.csv', 'r', encoding='utf-8') as csv_file:
    reader = csv.reader(csv_file)
    for line in reader:
        if line == []:
            continue
        row = line[0].split(';')
        class_, spec_list, spell_id, spell_name = row[0], row[1].split('+'), row[2], row[3]
        if spec_list[0] == 'all':
            spec_list = DB.query(f'select * from specs where lower(class)="{class_}"')
            spec_list = spec_list[0][1:4]
        for spec in spec_list:
            if 'restoration' in spec:
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
