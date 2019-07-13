from db_connect import Database

DB = Database()

current_version = DB.query('select data from system where variable="version"')[0][0]
print(type(current_version))
print(type(float(current_version)))
