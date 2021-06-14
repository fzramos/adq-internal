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
### PART 1: Set up the Database Schema for data profile upload
- Note: This program can upload to a variety of RDBMS including Snowflake, SQLite3
1. In command line, paste and run the command
```shell
pip install -r requirements.txt
```
2. Add a .env file to the project root with this format and your DB credentials:
```
SNOWFLAKE_ACCOUNT=xxxxx
SNOWFLAKE_USER=xxxxx
SNOWFLAKE_PASSWORD=xxxx
```
3. If using Snowflake as your RDBMS, run run the "validate_conn.py" program to make sure the Snowflake account credentials in your .env file are valid
4. In db_setup.py, change the line 6 argument to one of:
    - 'snowflake'
    - 'postgres'
    - 'sqlite'
5. Run db_setup.py
6. If this fails and you can't debug the issue, follow the instructions for "Manual Alembic Set-up". Alternatively, you can run the "sf_db_setup.sql" script in a new worksheet to get the landing databases, tables, and sequences set up for the program.

## PART 2: Create data profiles and upload them to DB
1. Unzip retail_banking.zip for sample CSV table files
2. Run "main.py" which both creates data profiles and uploads them to your RDBMS of choice.
3. In your RDBMS, run some select statements to see if the data has been uploaded successfully. For example:
```sql
// Run these to see if data profiles have been sucessfully uploaded
SELECT * FROM user;
SELECT * FROM data_profile;
SELECT * FROM column_profile;
SELECT * FROM data_type;

// See all data profiles connected to a user
SELECT u.user_id, dp.dp_id, c.COLUMN_NAME, dt.name AS "data_type", c.VALUE_COUNT, c.MISSING, 
c.PERCENT_MISSING, c.UNIQUE_COUNT, c.MAX_LENGTH, c.MIN_LENGTH, c.STDEV, c.MINIMUM, c.PERC25,
c.PERC50, c.PERC75, c.MAXIMUM
FROM column_profile c
JOIN data_type dt
ON c.type_id = dt.type_id
JOIN data_profile dp
ON dp.dp_id = c.dp_id
JOIN user u
ON u.user_id = dp.user_id
WHERE u.user_id = 0;
```

## OPTIONAL: Manual Alembic Set-up
- Purpose: Ultimate goal is to generalize this program so it will run on multiple types DBs (Snowflake, SQLite, PostgreSQL, etc). Key step to doing this is setting up the DB schema, tables in whatever type of DB it is. Alembic lets you use SQLAlchemy models of the tables you want for the schema then relatively easily use command line to create the schema on a variety of types of DBs. I want to use this fact to 1. Make a simple program to set up whatever type of DB you want (that is compatible with Alembic) 2. Then I can easily make a "create_engine" file that create an engine for whatever type of DB you want. 
1. In the project root in Anaconda Powershell
```shell
alembic init alembic
```
2. In new file "alembic.ini" add your sqlalchemy.url = xxxx
- Note that this is used in "profile_to_db" in the create_engine function call
3. In "alembic/env.py", add lines
```python
from models import Base
target_metadata = [Base.metadata]
```
4. In "alembic/env.py", comment out line
```python
target_metadata = None
```
5. If desired RDBMS is Snowflake, add:
```python
from alembic.ddl.impl import DefaultImpl

class SnowflakeImpl(DefaultImpl):
    __dialect__ = 'snowflake'
```
5. In Anaconda Powershell
```shell
alembic revision --autogenerate -m “First commit”
alembic upgrade head
```