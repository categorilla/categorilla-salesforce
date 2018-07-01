import time
import json
import logging

from categorilla import Categorilla
from salesforce import Cases

logger = logging.getLogger('categorilla-saleforce')
hdlr = logging.FileHandler('../categorilla-salesforce.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

logger.info("Starting new run.")

sf = Cases()
cat = Categorilla()

# get the cases
cases = sf.import_cases()

if not cases:
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
