# categorilla-salesforce

Categorilla-Salesforce is a python script that calls both the Salesforce and
Categorilla APIs, pulling Salesforce cases, assigning a category based on the
description, and inserting the category back into Salesforce.

**********
**SALESFORCE SETUP**

You will need to have a Salesforce account with the Service Cloud enabled.

On the Case object, you need:
* A "categorization status" custom picklist field with three values, representing:
    * Uncategorized cases (this should be the default value)
    * Cases where categorization is in progress
    * Categorized cases
* A custom text field to hold the category name

You will also need credentials for a Salesforce user to access the API. The
user will need at least read/write access to the Case object and related fields.


**CATEGORILLA SETUP**

You will need:
* A Categorilla account with a WEB API plan
* A project with categories assigned to case training data
* A model trained to this dataset
* Your project id and api token. You can find this in the project:
    1. Open the Categorilla project
    2. Click `Connect to API` in the upper-right corner
    3. Your token is listed at the top. If you have never done this before you
        will need to click `Refresh Token` to get one.
           *WARNING -- IF YOU REFRESH AN EXISTING TOKEN, THE OLD ONE WILL NO
            LONGER WORK*
    4. Your project ID can be found in the URL:
            `www.categorilla.com/app/code/[YOUR PROJECT ID]`


**CATEGORILLA-SALESFORCE SETUP**

The Categorilla-Salesforce script is intended to be run regularly via a cron
job.

Installation steps (Linux/Mac)
1. Clone the `categorilla-salesforce` repo
2. Open the project folder and create and activate a new environment (you will
    need virtualenv or your preferred env creation tool)
    `$ python3 -m virtualenv env`
    `$ source env/bin/activate`
3. Install requirements
    `$ pip install -r requirements.txt`
4. Create a copy of `development.ini_EXAMPLE`: `development.ini`
5. Fill in your information in `development.ini`:

`[salesforce]`
`username` Salesforce user credentials
`password` Salesforce user credentials
`token`    Salesforce user credentials
`is_sandbox` whether or not this is a Salesforce sandbox environment
`status_field` the custom picklist on the case for categorization state
`status_uncategorized` the picklist values
`status_inprogress` the picklist values
`status_complete` the picklist values
`category_field` the custom text field where the category will be added
`add_query` any additional filters you want on which cases are categorized:
    * If you do not want any additional filters, leave this blank:
        `add_query =`
    * If you wanted to only categorize new cases with the "billing" record type:
        `add_query = AND Status = 'New' AND RecordType.Name = 'billing'`

`[categorilla]`
`url_base` the base URL for the project api -- unless you have a custom instance
    of categorilla, this will be `https://www.categorilla.com/api/project/`
`project` the ID of the project. See CATEGORILLA SETUP for more details
`url_predict` should be set to `/predict/`
`url_poll` should be set to `/poll_predict/`
`token` your project token. See CATEGORILLA SETUP for more details
`num_predicts` The number of predictions to return. This should be set to 1 for
    most integrations
`confidence_threshold` How confident the prediction needs to be before this is
    added to the case. This should be set to a number between 0 and 1, with 1
    being absolute confidence and 0 being any prediction.

**ADD THE SCRIPT TO YOUR CRON TAB**
You can run the categorilla script at regular intervals using a cron job. You
will need to add the script to your crontab, using the python installed as part
of the virtual environment you created.

1. Open your crontab:
    `$ crontab -e`
2. Add a line to execute the cron.py script. You will need to fill in your paths.

    `* * * * * /YOURPATH/categorilla-salesforce/env/bin/python /YOURPATH/cateogrilla-salesforce/cateogrilla-salesforce/cron.py`
3. Save your file.
