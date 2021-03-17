import pandas as pd
# Imports SF Acct Sign-in Credentials
from sfCredentials import acct
# For Snowflake DB Connection
from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# models of tables for upload
from models import DataProfile, ColumnProfile

def test():
    data = pd.read_csv('dummy_profile.csv', sep=',')
    profile_to_db(data)

def profile_to_db(dp_df):
    engine = create_engine(URL(
        account = acct['SNOWFLAKE_ACCOUNT'],
        user = acct['SNOWFLAKE_USER'],
        password = acct['SNOWFLAKE_PASSWORD'],
        database = 'ADQ',
        schema = 'PUBLIC',
        warehouse = 'COMPUTE_WH',
        role='SYSADMIN'
    ))

    session = sessionmaker(bind=engine)()

    # connection = engine.connect()
    try:
        # connection.execute(<SQL>)
        newRow = DataProfile()
        session.add(newRow)
        session.commit()
    finally:
        # connection.close()
        engine.dispose()

if __name__ == "__main__":
    test()