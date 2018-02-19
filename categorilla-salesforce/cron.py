import time

from cateogrilla import Categorilla
from salesforce import Cases

sf = new salesforce.Cases()
cat = new categorilla.Categorilla()

# get the cases
cases = sf.import_cases()

# format cases

# call Categorilla


# try at most 60 times (1 minute)
for _ in range(60):
    time.sleep(1)

    # try to get predictions

    # if predictions are available post to salesforce and exit
    
