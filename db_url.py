from snowflake.sqlalchemy import URL as sfURL
import sqlalchemy.engine.url as url
from config import Config
import os

def create_db_url(db_type):
    # Get DB username and passwords
    db_config = Config()

    if db_type == 'snowflake':
        db_url = sfURL(
                account = db_config.SNOWFLAKE_ACCOUNT,
                user = db_config.SNOWFLAKE_USER,
                password = db_config.SNOWFLAKE_PASSWORD,
                database = 'ADQ',
                schema = 'PUBLIC',
                warehouse = 'COMPUTE_WH',
                role='SYSADMIN'
        )
    if db_type == 'sqlite':
        db_url = url.make_url(f'sqlite:///{os.path.abspath(os.getcwd())}\ADQ.db')
    
    return db_url