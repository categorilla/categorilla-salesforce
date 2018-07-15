try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser  # ver. < 3.0

import time
import os
import datetime
import json
import logging

from categorilla import Categorilla
from salesforce import Cases

# get config
config = ConfigParser()
config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                        '../',
                                        'development.ini'))

# set log path
log_path = config.get('general', 'log_path')
today = datetime.datetime.today().strftime('%Y-%m-%d')
log_filename = '%s/categorilla-salesforce-%s' % (log_path, today)

# set up logging
logger = logging.getLogger('categorilla-saleforce')
hdlr = logging.FileHandler(filename=os.path.abspath(log_filename))
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

logger.info("****Starting new run****")

sf = Cases(config, logger)
cat = Categorilla(config, logger)

# get the cases
cases = sf.import_cases()

if not cases:
    logger.info("No categorizable cases found.")
    logger.info("****Ending run****")
    quit()

# call Categorilla
predict_response = json.loads(cat.send_text(cases))
if type(predict_response) is str:
    logger.error("predict response: %s" % predict_response)
    quit()

# try at most 60 times (1 minute)
for _ in range(60):
    time.sleep(1)

    # try to get predictions
    poll_response = json.loads(cat.get_predictions(predict_response))
    logger.info("poll response: %s" % poll_response)

    # if predictions aren't availble, try again in a second
    if poll_response['status'] != 'done':
        continue

    # otherwise, update to Salesforce
    sf.update_cases(poll_response['records'])
    break

logger.info("****Ending run****")
