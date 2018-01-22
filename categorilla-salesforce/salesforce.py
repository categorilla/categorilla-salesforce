try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser  # ver. < 3.0

# https://pypi.python.org/pypi/simple-salesforce
from simple_salesforce import Salesforce


class Cases:

    def __init__(self):
        config = ConfigParser()
        config.read('../development.ini')
        USERNAME = config.get('salesforce', 'username')
        PASSWORD = config.get('salesforce', 'password')
        TOKEN = config.get('salesforce', 'token')
        IS_SANDBOX = config.getboolean('salesforce', 'is_sandbox')
        CLIENT_ID = 'Categorilla'

        self.sf = Salesforce(username=USERNAME,
                             password=PASSWORD,
                             security_token=TOKEN,
                             sandbox=IS_SANDBOX,
                             client_id=CLIENT_ID)

        self.STATUS_FIELD = config.get('salesforce', 'status_field')
        self.STATUS_UNCATEGORIZED = \
            config.get('salesforce', 'status_uncategorized')
        self.STATUS_INPROGRESS = \
            config.get('salesforce', 'status_inprogress')
        self.STATUS_COMPLETE = \
            config.get('salesforce', 'status_complete')
        self.ADD_QUERY = config.get('salesforce', 'add_query')

    def import_cases(self):
        
        case_query = 'SELECT ID, Description \
                      FROM Case WHERE' \
                      + self.STATUS_FIELD \
                      + ' = "' \
                      + self.STATUS_UNCATEGORIZED \
                      + '"' \
                      + add_query

        return self.sf.query(case_query)

    # case_data = [{'Id': '0030000000AAAAA', 'Category': '14'},
    #  {'Id': '0030000000BBBBB', 'Category': 'asdf'}]
    def update_cases(self, case_data):
        return(self.sf.bulk.Contact.update(case_data))
