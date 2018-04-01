try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser  # ver. < 3.0

# https://pypi.python.org/pypi/simple-salesforce
from simple_salesforce import Salesforce, exceptions as sfexcept


class Cases:

    def __init__(self):
        config = ConfigParser()
        config.read('../development.ini')
        USERNAME = config.get('salesforce', 'username')
        PASSWORD = config.get('salesforce', 'password')
        TOKEN = config.get('salesforce', 'token')
        IS_SANDBOX = config.getboolean('salesforce', 'is_sandbox')
        CLIENT_ID = 'Categorilla'

        try:
            self.sf = Salesforce(username=USERNAME,
                                 password=PASSWORD,
                                 security_token=TOKEN,
                                 sandbox=IS_SANDBOX,
                                 client_id=CLIENT_ID)
        except sfexcept.SalesforceAuthenticationFailed as err:
            print('Salesforce Error: {0}'.format(err))
            print('Username: {0}'.format(USERNAME))
            print('Password: {0}'.format(PASSWORD))
            print('Token: {0}'.format(TOKEN))
        except:
            print('Unexpected error:', sys.exc_info()[0])
            raise

        self.STATUS_FIELD = config.get('salesforce', 'status_field')
        self.STATUS_UNCATEGORIZED = \
            config.get('salesforce', 'status_uncategorized')
        self.STATUS_INPROGRESS = \
            config.get('salesforce', 'status_inprogress')
        self.STATUS_COMPLETE = \
            config.get('salesforce', 'status_complete')
        self.CATEGORY_FIELD = config.get('salesforce','category_field')
        self.ADD_QUERY = config.get('salesforce', 'add_query')
        self.THRESHOLD = config.getfloat('categorilla','confidence_threshold')


    def import_cases(self):

        # get uncategorized cases
        case_query = 'SELECT ID, Description ' \
                     'FROM Case WHERE ' \
                      + self.STATUS_FIELD \
                      + ' = \'' \
                      + self.STATUS_UNCATEGORIZED \
                      + '\' ' \
                      + self.ADD_QUERY

        try:
            res = self.sf.query(case_query)
            num_records = res['totalSize']
            print('{0} records returned.'.format(num_records))
        except sfexcept.SalesforceMalformedRequest as err:
            print('Query error: {0}'.format(err))
            print('Query: {0}'.format(case_query))
            return
        except:
            print('Unexpected error:', sys.exc_info()[0])
            raise

        # no records, exit
        if not num_records > 0:
            return

        '''
        Formatting for categorilla
        {
            "top_n":1,
            "records": [
               ["id1", "Text"],
               ["id2", "More text"]
            ]
        }
        '''

        # formating for update and categorilla
        cases = []
        formatted_cases = []
        for record in res['records']:
            formatted_cases.append([record['Id'], record['Description']])
            cases.append({'Id' : record['Id'],
                          'Description' : record['Description'],
                          self.STATUS_FIELD : self.STATUS_INPROGRESS})

        # update them as in progress in SF
        if cases:
            try:
                response = self.sf.bulk.Case.update(cases)
                print(response)
            except sfexcept.SalesforceMalformedRequest as err:
                print('Update error: {0}'.format(err))
                print('Update: {0}'.format(cases))
            except:
                print('Unexpected error:', sys.exc_info()[0])
                raise

        return formatted_cases


        '''
        from categorilla will be in format:
            "records": [
                [
                    "id1",
                    [
                        {
                            "category": "agri-business",
                            "confidence": 0.760093629360199
                        }
                    ]
                ],
                [
                    "id2",
                    [
                        {
                            "category": "agri-business",
                            "confidence": 0.760093629360199
                        }
                    ]
                ]
            ]

        Needs to be in format

        case_data = [{'Id': '0030000000AAAAA', 'Category__c': '14',
        Cateogrization_Status__c = "Categorized"},
        {'Id': '0030000000BBBBB', 'Category__c': 'asdf'}]
        '''

    def update_cases(self, records):
        case_data = []

        # reformat for salesforce
        for record in records:
            # if(record[1][0].confidence >= self.THRESHOLD)
            case_data.append({'Id' : record[0],
                          self.CATEGORY_FIELD : record[1][0].category,
                          self.STATUS_FIELD : self.STATUS_COMPLETE})

        return(self.sf.bulk.Case.update(case_data))
