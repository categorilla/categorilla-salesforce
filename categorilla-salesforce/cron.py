import time

from categorilla import Categorilla
from salesforce import Cases

sf = new salesforce.Cases()
cat = new categorilla.Categorilla()

# get the cases
cases = sf.import_cases()

# call Categorilla
predict_response = cat.send_text(cases)

# try at most 60 times (1 minute)
for _ in range(60):
    time.sleep(1)

    # try to get predictions
    poll_response = cat.get_predictions(predict_response)

    # if predictions aren't availble, try again in a second
    if poll_response.status != 'done':
        continue

    # otherwise, update to Salesforce
    sf.update_cases(poll_response.records)
    break
