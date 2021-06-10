import pandas as pd
# Imports SF Acct Sign-in Credentials
from sfCredentials import acct
# For Snowflake DB Connection
from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# models of tables for upload
from models import DataProfile, ColumnProfile, DataType
from config import Config
from db_url import create_db_url

def test():
    data = pd.read_csv('dummy_profile.csv', sep=',')
    profile_to_db(data, 0, 'snowflake')

def profile_to_db(dp_df, user_id, db_type):
    engine = create_engine(create_db_url(db_type))

    session = sessionmaker(bind=engine)()

    try:
        # Creating a new data profile row in the data_profile table
        newProfile = DataProfile(user_id = user_id)
        # Note, newProfile dp_id isn't created until commited since SF creates the value on insert
        session.add(newProfile)

        session.commit()
        
        # Adding data profile rows to column_profile table with a new column of dp_id
        # so rows are related by their new data profile id 
        dp_df["dp_id"] = newProfile.dp_id
        dp_df.to_sql('column_profile', engine, if_exists='append', index=False)
        print("Data profile uploaded sucessfully.")
    finally:
        # connection.close()
        engine.dispose()

if __name__ == "__main__":
    test()