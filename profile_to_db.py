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
    # TODO add parameters for parent_table_id and owner_id/user_id
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

    try:
        # Creating a new data profile row in the data_profile table
        # TODO parent_id = some number
        newProfile = DataProfile()
        # Note, newProfile dp_id isn't created until commited since SF creates the value on insert
        session.add(newProfile)
        session.commit()
        
        # Adding data profile rows to column_profile table with a new column of dp_id
        # so rows are related by their new data profile id 
        dp_df["dp_id"] = newProfile.dp_id
        dp_df.to_sql('column_profile', engine, if_exists='append', index=False)

    finally:
        # connection.close()
        engine.dispose()

if __name__ == "__main__":
    test()