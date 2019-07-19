import requests


class Server():
    def __init__(self):
        self.token = None
        self.options = None

    def connect(self, url, key, hwid):
        try:
            response = requests.get(url + f'auth/?key={key}&hwid={hwid}').json()
            status = response['status']
            error = response['error']
            self.token = response['token']
            self.options = response['options']
            if error:
                print('error')
                return False
            else:
                return True
        except:
            print('json error')
            return False

