import requests


class Server():
    def __init__(self):
        import uuid
        self.token = None
        self.options = None
        self.hwid = uuid.UUID(int=uuid.getnode())
        self.url = 'http://127.0.0.1:8000/'
    def connect(self, key):
        try:
            response = requests.get(self.url + f'api/auth/?key={key}&hwid={self.hwid}').json()
            error = response['error']
            self.token = response['token']
            self.options = response['options']
            if error:
                print(f'error: {error}')
                return 'token'
            return True
        except Exception as E:
            print(f'error: {E}')
            return 'server'

    def check_update(self):
        response = requests.get(self.url + f'api/update_check/?token={self.token}&hwid={self.hwid}').json()
        error = response['error']
        if error:
            print(error)
            return False
        else:
            return response['global_version']

    def load_updater(self):
        response = requests.get(self.url + f'api/update_soft/?file=updater')
        with open('update.exe', 'wb') as f:
            f.write(response.content)
            return True

    def token_update(self, main):
        response = requests.get(self.url + f'api/token_update/?token={self.token}&hwid={self.hwid}').json()

        error = response['error']
        if not error:
            self.token = response['token']
        else:
            print(response)
            print(main)
            import ctypes
            #main.hide()
            ctypes.windll.user32.MessageBoxW(0, "You has been disconnected from server", "Disconnected", 0)
            import os
            os._exit(1)

    def bug_report(self, file):
        request = requests.post(self.url + f'api/bug_report/?token={self.token}&hwid={self.hwid}',
                                 files={'uploads': file})
        return request.status_code


try:
    import httplib
except:
    import http.client as httplib

def internet_on():
    conn = httplib.HTTPConnection("www.google.com", timeout=5)
    try:
        conn.request("HEAD", "/")
        conn.close()
        return True
    except:
        conn.close()
        return False