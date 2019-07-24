import requests


class Server():
    def __init__(self):
        import uuid
        self.token = None
        self.options = None
        self.hwid = uuid.UUID(int=uuid.getnode())

    def connect(self, url, key):
        try:
            response = requests.get(url + f'api/auth/?key={key}&hwid={self.hwid}').json()
            error = response['error']
            self.token = response['token']
            self.options = response['options']
            if error:
                print('error')
                return False
            return True
        except:
            print('json error')
            return False

    def check_update(self, url):
        response = requests.get(url + f'api/update_check/?token={self.token}&hwid={self.hwid}').json()
        error = response['error']
        if error:
            print(error)
            return False
        else:
            return response['global_version']

    def load_updater(self, url):
        response = requests.get(url + f'api/update_soft/?file=updater')
        with open('update.exe', 'wb') as f:
            f.write(response.content)
            return True
