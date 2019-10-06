import ctypes
import requests
ctypes.windll.user32.MessageBoxW(0, "Starting download last version of program in this directory.\nEstimated downnload time ~20s.", "Updating", 0)
url = 'https://justbecome.pro/'
response = requests.get(url + f'api/update_soft/?file=exe')
with open('script.exe', 'wb') as f:
    f.write(response.content)
ctypes.windll.user32.MessageBoxW(0, "Updated! Now you can start the script", "Updated!", 0)
