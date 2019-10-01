import requests
url = 'https://justbecome.pro/'
response = requests.get(url + f'api/update_soft/?file=exe')
with open('script.exe', 'wb') as f:
    f.write(response.content)
import ctypes
ctypes.windll.user32.MessageBoxW(0, "Updated! Now you can start the script", "Updated!", 0)
