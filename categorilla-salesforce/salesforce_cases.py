try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser  # ver. < 3.0

# https://pypi.python.org/pypi/simple-salesforce
from simple_salesforce import Salesforce


def case_test():
    config = ConfigParser()
    config.read('../development.ini')
    USERNAME = config.get('salesforce', 'username')
    PASSWORD = config.get('salesforce', 'password')
    TOKEN = config.get('salesforce', 'token')
    IS_SANDBOX = config.getboolean('salesforce', 'is_sandbox')
    CLIENT_ID = 'Categorilla'

    sf = Salesforce(username=USERNAME,
                    password=PASSWORD,
                    security_token=TOKEN,
                    sandbox=IS_SANDBOX,
                    client_id=CLIENT_ID)

    case_query = 'SELECT ID FROM Case'
    cases = sf.query(case_query)

    print(cases)
