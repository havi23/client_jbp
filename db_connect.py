import sqlite3
import os
from bin.resource_to_exe import resource_path

class Database:
    def __init__(self):
        appdata = os.path.join(os.environ['APPDATA'], 'ApplicationData')
        if not os.path.exists(appdata):
            os.makedirs(appdata)
            from shutil import copyfile
            copyfile(resource_path('data'), os.path.join(dir_path, 'data'))
        file_path = os.path.join(appdata, 'data')
        self._conn = sqlite3.connect(file_path)
        #self._conn = sqlite3.connect(database=resource_path('data'))
        self._cursor = self._conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.commit()
        self.connection.close()

    @property
    def connection(self):
        return self._conn

    @property
    def cursor(self):
        return self._cursor

    def commit(self):
        self.connection.commit()

    def execute(self, sql, params=None):
        self.cursor.execute(sql, params or ())

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def query(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.fetchall()