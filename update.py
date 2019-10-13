import ctypes
import requests
from db_connect import Database


ctypes.windll.user32.MessageBoxW(0, "Starting download last version of program in this directory.\nEstimated downnload time ~20s.", "Updating", 0)
url = 'https://justbecome.pro/'
response = requests.get(url + f'api/update_soft/?file=exe')
with open('script.exe', 'wb') as f:
    f.write(response.content)

DB = Database()
global_version = float(DB.query('select data from system where variable="global_version"')[0][0])
DB.execute(F'UPDATE system SET DATA="{global_version}" WHERE VARIABLE="version"')
DB.commit()
ctypes.windll.user32.MessageBoxW(0, "Updated! Now you can start the script", "Updated!", 0)
