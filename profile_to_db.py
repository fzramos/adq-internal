import pandas as pd
from sfInfo import acct

def test():
    data = pd.read_csv('dummy_profile.csv', sep=',')
    profile_to_db(data)

def profile_to_db(dp_df):
    pass

if __name__ == "__main__":
    test()