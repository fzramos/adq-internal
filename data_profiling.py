import numpy as np
import pandas as pd
import seaborn as sns

def test():
    # Only runs if this file is run. Tests data_profile function 
    result_df = data_profiling('retail_banking/completedacct.csv')
    result_df.to_csv('out.csv', index=False)

def data_profiling(file_path, type_threshold = 0.5):
    """
    Get info about a csv table columns
    Info includes column's name, data type, count, missing count, % missing, unique count, max and min length, and summary statistics if numeric column

    Parameters
    ----------
    file_path: relative or absolute file path to the csv
    type_threshold: % limit of columns with NaN rows if forced to datetime data type

    Returns
    -------
    Pandas dataframe containing each column's profile as a row
    """

    data=pd.read_csv(file_path, sep=',')

    # this is a DataFrame where our summary statistics results go
    result=pd.DataFrame(data.columns, columns=['Column Names'])

    types=[]
    length=[]
    missing=[]
    percent_missing=[]
    unique_count=[]

    max_length=list(dict([(v, data[v].apply(lambda r: len(str(r)) if r!=None else 0).max())for v in data.columns.values]).values())
    min_length=list(dict([(v, data[v].apply(lambda r: len(str(r)) if r!=None else 0).min())for v in data.columns.values]).values())

    for col in data.columns:
        # column type inferring
        # Using numbers because on data profile upload to DB this column refer to foreign keys of a data type table 
        # { 'int': 0, 'float': 1, 'str': 2, 'datetime': 3, 'error': 4}
        if (data.dtypes[col] == 'object') or (data.dtypes[col] == 'bool'):
            # attempting to cast the column as datetime type            
            col_date_cast = pd.to_datetime(data[col], errors='coerce')
            date_nan_per = np.sum(pd.isnull(col_date_cast)) * 1.0 / len(col_date_cast)
            if date_nan_per < (1.0 - type_threshold):
                types.append(3) # datetime
            else:
                types.append(2) # str
        elif data.dtypes[col] == 'datetime64':
            types.append(3) # datetime
        elif data.dtypes[col] == "int64":
            types.append(0) # int
        elif data.dtypes[col] == "float64":
            types.append(1) # float
        else:
            types.append(4) # error
        
        # additional analysis for data profile
        length.append(len(data[col]))
        missing.append(data[col].isna().sum())
        percent_missing.append(data[col].isna().sum()/len(data[col]))
        unique_count.append(data[col].nunique())

    result["type_id"]=types
    result["value_count"]=length
    result["missing"]=missing
    result["percent_missing"]=percent_missing
    result["unique_count"]=unique_count
    result["max_length"]=max_length
    result["min_length"]=min_length

    # list of dtypes to include, types to analyze with describe 
    # TODO include more numeric dtypes?
    include =['float64', 'int64', 'Int8', 'Int16', 'Int32', 'UInt8', 'UInt16', 'UInt32', 'UInt64'] 

    # adding summary stats (except for count stat which has already been added to result df)
    try:
        des=data.describe(include = include)[1:].transpose()
    except:
        # if no int, float columns, creating empty summary stats columns for profile
        des = pd.DataFrame(columns=['mean', 'std', 'min', '25%', '50%', '75%', 'max'])
    # renaming percentage column headers
    des.rename({'25%': 'perc25', '50%': 'perc50', '75%': 'perc75', 'std': 'stdev', 'min': 'minimum', 'max': 'maximum'}, axis=1, inplace=True)
    result=result.set_index('Column Names').join(des)
    column_name=result.index.values
    result.insert(loc=0,column="column_name",value=column_name)

    # print(result)
    print('Data profile created successfully.')
    return result

if __name__ == "__main__":
    test()