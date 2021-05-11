## Automated Data Quality Program
This program ingests a CSV table, creates data profiles of each column of the table, then sends the data profile to a Snowflake database

## Key Files
* data_profiling.py: Ingests CSV file and prints and returns a data profile with various descriptive details about the data within the columns of the CSV table
* profile_to_db.py: Takes a CSV or Dataframe of a data profile and uploads it to a Snowflake database (assuming connection is valid)
* validate_conn.py: Validates the credentials of the "sfCredentials.py" file, making sure the successfully connect to a Snowflake Account
* sfCredentials.py: **Must be created by user.** Holds your Snowflake account credentials 
* sf_db_setup.sql: SQL script needed to set up the landing database and tables on your account for this program
* main.py: Uses functions from "data_profiling.py" and "profile_to_db.py" to both create a data profile from a CSV file and uploads the data profile to your Snowflake account.

## Steps to get up and running
1. pip install -r requirements.txt
2. Unzip retail_banking.zip for sample CSV table files
3. Create "sfCredentials.py" with your snowflake account credentials
    - Format of file: 
        acct = {
            'SNOWFLAKE_ACCOUNT': 'account_id.region.cloud_provider',
            'SNOWFLAKE_USER': 'username',
            'SNOWFLAKE_PASSWORD': 'password'
        }
4. Run the "validate_conn.py" program to make sure the Snowflake account credentials you added are valid
5. In your Snowflake account, run the "sf_db_setup.sql" script in a new worksheet to get the landing databases, tables, and sequences set up for the program
6. Run "main.py" to send a data profile to your Snowflake account
7. In a Snowflake Worksheet, run some select statements to see if the data has been uploaded successfully