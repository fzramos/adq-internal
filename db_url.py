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
    elif db_type == 'sqlite':
        db_url = url.make_url(f'sqlite:///{os.path.abspath(os.getcwd())}\ADQ.db')
    elif db_type == 'postgres':
        db_url = url.make_url(
            f'postgres://{db_config.POSTGRES_USER}'\
            + ':{db_config.POSTGRES_PASSWORD}@localhost'\
            + ':5432/ADQ'
        )
    # postgres://user:secret@localhost:5432/mydatabasename 
    return db_url