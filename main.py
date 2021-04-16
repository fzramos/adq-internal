from data_profiling import data_profiling
from profile_to_db import profile_to_db

def main():
    #  file path of data in csv format
    file_path = 'retail_banking/completedcard.csv'
    
    # If incoming data is related to data previously profiled
    # then add the parent_id of that data profile, otherwise
    # leave null and a new parent_id will be auto-generated
    parent_id = None

    # Id of the user/owner of account that submitted this data for profiling
    # Assuming user id has already been added to User table
    user_id = 0 

    # creates data profile
    dp_df = data_profiling(file_path)

    # upload profile to Snowflake
    profile_to_db(dp_df, parent_id, user_id)

main()