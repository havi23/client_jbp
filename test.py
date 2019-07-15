from db_connect import Database

# TODO В разработке
DB = Database()

current_version = DB.query('select data.db from system where variable="version"')[0][0]
print(type(current_version))
print(type(float(current_version)))
