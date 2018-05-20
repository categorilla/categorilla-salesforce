try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser  # ver. < 3.0

import requests
import json
import logging

class Categorilla:

    def __init__(self):
        config = ConfigParser()
        config.read('../development.ini')
        self.BASE = config.get('categorilla', 'url_base')
        self.PROJECT = config.get('categorilla', 'project')
        self.PREDICT = config.get('categorilla', 'url_predict')
        self.POLL = config.get('categorilla', 'url_poll')
        self.TOKEN = config.get('categorilla', 'token')
        self.TOP_N = config.getint('categorilla', 'num_predicts')


    def send_text(self, records):
        url = self.BASE + self.PROJECT + self.PREDICT
        body = {'confidence': True, 'top_n': self.TOP_N, 'records': records}
        headers = {'Authorization': 'Token {}'.format(self.TOKEN),
                   'Content-Type': 'application/json'}
        logging.debug(body)
        r = requests.post(url, data=json.dumps(body), headers=headers)

        return r.text


    def get_predictions(self, body):
        url = self.BASE + self.PROJECT + self.POLL
        headers = {'Authorization': 'Token {}'.format(self.TOKEN),
                   'Content-Type': 'application/json'}
        r = requests.post(url, data=json.dumps(body), headers=headers)
        return r.text
