import os

# key to allowing .env to act like environmental variables
from dotenv import load_dotenv
load_dotenv()

class Config(object):
    SNOWFLAKE_ACCOUNT = os.environ.get('SNOWFLAKE_ACCOUNT')
    SNOWFLAKE_USER = os.environ.get('SNOWFLAKE_USER')
    SNOWFLAKE_PASSWORD = os.environ.get('SNOWFLAKE_PASSWORD')