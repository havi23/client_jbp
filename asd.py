from db_connect import Database

DB = Database()
spec_list = DB.query('select spec_1, spec_2, spec_3, spec_4 from specs')
print(spec_list)
s_list = []
for class_ in spec_list:
    if class_[0] is not None:
        s_list.append(class_[0])
    if class_[1] is not None:
        s_list.append(class_[1])
    if class_[2] is not None:
        s_list.append(class_[2])
    if class_[3] is not None:
        s_list.append(class_[3])

print(s_list)


for table in s_list:
    DB.query(f'''
    
    create table if not exists {table}
(
  spell    varchar(150) not null
    constraint {table}_pk
    primary key,
  color    varchar(8)   not null,
  bind     int default NULL,
  critical int default 0 not null
);
    ''')
