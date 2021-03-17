from data_profiling import data_profiling
from profile_to_db import profile_to_db

def main():
    # create data profile
    dp_df = data_profiling('retail_banking/completedcard.csv')

    # upload profile to Snowflake
    profile_to_db(dp_df)

main()
