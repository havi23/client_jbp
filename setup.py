import requests
import ctypes
url = 'https://justbecome.pro/'
ctypes.windll.user32.MessageBoxW(0, "Starting download last version of program in this directory.\nEstimated downnload time ~20s.", "Download", 0)
response = requests.get(url + f'api/update_soft/?file=exe')
with open('script.exe', 'wb') as f:
    f.write(response.content)
ctypes.windll.user32.MessageBoxW(0, "The last version of program has been downloaded as script.exe!", "Success", 0)
