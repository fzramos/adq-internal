from data_profiling import data_profiling
from profile_to_db import profile_to_db

def main():
    #  file path of data in csv format
    file_path = 'retail_banking/completedcard.csv'
    
    # RDBMS type: 'snowflake' OR 'sqlite'
    db_type = 'sqlite'

    # Id of the user/owner of account that submitted this data for profiling
    # Assuming user id has already been added to User table
    user_id = 0

    # creates data profile
    dp_df = data_profiling(file_path)

    # upload profile to Snowflake
    profile_to_db(dp_df, user_id, db_type)

main()