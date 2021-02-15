import numpy as np
import pandas as pd
import seaborn as sns

def simplified(file_path):
    # this automatically turns csv into a dataframe
    # including knowing what the columns names are and the column datatypes!
    data = pd.read_csv(file_path, sep=',')
    print(data.columns)
    print(data.columns.values)
    print(list(data.columns.tolist())) # this makes the column names into a list
    print(data.dtypes)

    result = pd.DataFrame(data.columns, columns = ['Column Names'])
    print(result)

    # result=pd.DataFrame(data.columns, columns=['color', 'count'])
    # return data
    
    # so v is basically just color, count, column names
    # data[v] is data['column name'] which returns all column values
    # and the .apply is just finding the max length of the column values
    # and if a particular column value (r) is Null/None then just call that 0
    # so ultimately a list of column names and biggest length of all of that column elements
    # output if you remove list, dict, and end .values()
        # [('color', 4), (' count', 1)]
    # with dict: {'color': 4, ' count': 1}
    # with values added at end: dict_values([4, 1])
    # with list added on top: [4, 1]

    # so basically this code function is using a list comprehension to create a 
    # list of TUPLES with column name and the columns max lengthed value
    # then turn that into a dict, only get the values of the dict, then finally a list
    # of the max lengthed values of each column of the imported data
    max_length=[v for v in data.columns.values]
    max_length=[(v, data[v].apply(lambda r: len(str(r)) if r!=None else 0).max()) \
        for v in data.columns.values]

    max_length=list(dict([(v, data[v].apply(lambda r: len(str(r)) if r!=None else 0).max()) \
        for v in data.columns.values]).values())
    min_length=list(dict([(v, data[v].apply(lambda r: len(str(r)) if r!=None else 0).min())\
        for v in data.columns.values]).values())

    print()
    # key: dtypes property of a DataFrame are the COLUMN datatypes. Very critical
    print(data.dtypes)
    print(len(data.dtypes))

    result["Data_Types"]=['string', 'int']
    print(result)
    print()

    # this gets all the summary statistics and puts it into several columns
    # summary stats transposed
    #        count  mean       std  min   25%  50%   75%  max
    # count    2.0   1.5  0.707107  1.0  1.25  1.5  1.75  2.0
    des = data.describe().transpose()

    print()
    print(data.columns)
    print(data.columns.values)
    # note: you can iterate though the data.columns although it's not like a normal list
    # its really a vector/numpy matrix which is why it has no commas
    for i in data.columns:
        print(data[i])

    print()
    print(result)
    print(des)
    print()
    # NOTE: Since colors row is a string, summary stats make sense
    # so join makes all summary stats say NaN
    # will that cause problems when putting it in SQL?
    # NO: because test of 'isna()' shows NaN is counted as null value
    result=result.set_index('Column Names').join(des)
    print(result)
    print()
    # This remove the annoying 0, 1 from front of DF
    column_name=result.index.values
    print(column_name)

    result.insert(loc=0,column="Column_Name",value=column_name)
    print(result)

    missing = []
    for i in result.columns:
        missing.append(result[i].isna().sum())

    print(missing)
simplified('test.csv')
# using relative path


def data_profiling(file_path):

        data=pd.read_csv(file_path, sep=',')

        # this is a DataFrame for where our summary statistics results go
        result=pd.DataFrame(data.columns, columns=['Column Names'])

        types=[]
        length=[]
        missing=[]
        percent_missing=[]
        unique_count=[]

        max_length=list(dict([(v, data[v].apply(lambda r: len(str(r)) if r!=None else 0).max())for v in data.columns.values]).values())
        min_length=list(dict([(v, data[v].apply(lambda r: len(str(r)) if r!=None else 0).min())for v in data.columns.values]).values())
        for i in data.dtypes:
            if str(i) == "int64":
                types.append("int")
            elif str(i) == "float64":
                types.append("float")
            elif str(i) == "object":
                types.append("string")
        for i in data.columns:
            length.append(len(data[i]))
            missing.append(data[i].isna().sum())
            percent_missing.append(data[i].isna().sum()/len(data[i]))
            unique_count.append(data[i].nunique())

        result["Data_Types"]=types
        result["Count"]=length
        result["Missing"]=missing
        result["Percent_Missing"]=percent_missing
        result["Unique_Count"]=unique_count
        result["Max_Length"]=max_length
        result["Min_Length"]=min_length
        #result["Mean"]=mean_val

        des=data.describe().transpose()

        result=result.set_index('Column Names').join(des)
        column_name=result.index.values
        result.insert(loc=0,column="Column_Name",value=column_name)
        print(result)
        result.to_csv('out.csv', index=False)

        # in the result there are 2 count's, 2nd count is for numberic columns
        return result

data_profiling('test.csv')
