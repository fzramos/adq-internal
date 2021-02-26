## 02/7/2020 
Add date type to column data type categorization YES
Should we add memory usage stats to profile? NO
Correlation/data comparison within column EXPLORE
Correlation bw column - Important in the future (not in the profile)

Question: Results dataframe has 2 count columns, 1 for total data point, one from summary statistics. Keep both with a rename?
    Answer: Remove second
Question: Are we focusing on making singular data profiles and putting them on SQL or are we comparing data profiles?
    Answer: Comparing is for later
Question: Should we be tagging the Data Profiles?
    Answer: Make table giving data profiles a parent grouping if they are from the same data set but at different times/new data points
Question: Should we work on graphing/visualizing the Data Profiles?

## 02/15/2020  
- COMPLETED: Meet with Twinkle: Tell her to use nice UI templates and to look at DataBuck for an idea of end goal
    - Tell her were going to make a API for the front end UI to pull the data from
- COMPLETED: Look for new 2-3 good Kaggle datasets for sample data testing (probably Banking datasets)
- COMPLETED: Add code to data_profile for date type checking
- Research to see if correlation coefficient is added in other ADQ examples online
- COMPLETED: Remove 2nd 'count' column from data_profile output
- Build database in Snowflake
- Connect program to Snowflake database and send data profiles there




