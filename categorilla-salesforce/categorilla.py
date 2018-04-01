try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser  # ver. < 3.0

import requests

class Categorilla:

    def __init__(self):
        config = ConfigParser()
        config.read('../development.ini')
        self.BASE = config.get('cateogrilla', 'url_base')
        self.PROJECT = config.get('cateogrilla', 'project')
        self.PREDICT = config.get('cateogrilla', 'url_predict')
        self.POLL = config.get('cateogrilla', 'url_poll')
        self.TOKEN = config.get('cateogrilla', 'token')
        self.TOP_N = config.getint('categorilla', 'num_predicts')


    def send_text(self, records):
        url = self.BASE + self.PROJECT + self.PREDICT
        body = {'top_n': TOP_N, 'records': records}
        headers = {'Authorization': 'Token {}'.format(self.TOKEN)}
        r = requests.post(url, data=body, headers=headers)
        return r.text


    def get_predictions(self, body):
        url = self.BASE + self.PROJECT + self.POLL
        headers = {'Authorization': 'Token {}'.format(self.TOKEN)}
        r = requests.post(url, data=body, headers=headers)
        return r.text
