import pandas as pd
import numpy as np
import os


def read_csv_waipara_aws(file_path):
    """Read in the Waipara AWS weather station data with initial filtering
    """

    # read in the entire file, first row becomes column labels
    df = pd.read_csv(file_path)

    # drop second row (first row of data), since its just an extension of header
    df = df.drop(labels=[0], axis=0)

    # drop unecessary columns, which is a lot of them
    df = df.drop(labels=['Julian day', 'Unnamed: 0', 'Battery', '20cm soil T', 'Solar rad', 'rainfall', 'Wind speed',
       'Vector speed', 'Vector dir', 'SD dir', 'PAR', 'Cumulative', 'Tmean', 'Unnamed: 18'], axis=1)

    # drop additional columns, so I can focus on just temperature
    df = df.drop(labels=['RH', '1.5m air T', '0.7m RH'], axis=1)

    # iterate across each row to create a suitable date value
    dates = []
    for index, row in df.iterrows():

        # create formatted date string based on current time
        if len(str(row['Time'])) == 3:
            new_date = row['Date'] + " 000" + str(row['Time'])
        elif len(str(row['Time'])) == 4:
            new_date = row['Date'] + " 00" + str(row['Time'])
        elif len(str(row['Time'])) == 5:
            new_date = row['Date'] + " 0" + str(row['Time'])
        elif len(str(row['Time'])) == 6:
            new_date = row['Date'] + " " + str(row['Time'])
        
        # convert to a pandas datetime dtype
        dates.append(pd.to_datetime(new_date, format='%Y-%m-%d %H%M.%S'))

    # save the new date column and drop the no longer needed time column
    df['Date'] = dates
    df = df.drop(labels=['Time'], axis=1)

    # ensure standardised name for Tair column that we will use for modelling
    df = df.rename(columns={"0.7m air T": "Tair"}, errors="raise")

    # return the filtered df
    return df


def create_feature_target_df(df, hour_diff_to_store):
    """Creates dataframe with features and target variable

    Parameters:
    df (dataframe): Original dataframe
    hour_diff_to_store (range): past observations to store (hours different)

    Returns:
    df2 (dataframe): Features and target variable dataframe.    
    """
    # create a dictionary of temperatures to store for each date
    features_all = {}

    # iterate across all rows of original dataframe
    for i in range(len(df)):

        # create empty list, will store the past temperatures in here
        features_current = []

        # store current date
        current_date = df['Date'].iloc[i]

        # only continue if current date is on the hour i.e. disregarding half-hourly data
        if current_date.minute == 0:

            # iterate all prior rows, working backwards, until max number of features stored
            for j in range(i):

                # work out row number of past observation to consider
                index = i-j-1

                # work out time difference to this past observation
                compare_date = df['Date'].iloc[index]
                time_diff = pd.Timedelta(current_date-compare_date).total_seconds()/3600.0

                # if time difference is an integer and in range of past times to store, store it
                if time_diff.is_integer() and (int(time_diff) in hour_diff_to_store):
                    features_current.append(df['Tair'].iloc[index])

                # check if we have already stored max expected number of features, to save time
                if len(features_current) == len(hour_diff_to_store):
                    break

            # only store row in final dict if it has full number of expected features
            if len(features_current) == len(hour_diff_to_store):
                
                # append target variable (i.e. current temp) to features list
                features_current.append(df['Tair'].iloc[i])

                # create new entry in dictionary
                features_all[current_date] = features_current

    # create new dictionary including all features and target variable
    df2 = pd.DataFrame.from_dict(features_all, orient='index')

    # set feature names based on stored hours
    column_names = []
    for i in hour_diff_to_store:
        column_names.append("Tair"+str(i))

    # set the target variable name
    column_names.append("Tair")

    # if any data was stored in dictionary, set the column names
    if df2.shape[1] == len(column_names):
        df2.columns = column_names

    return df2



def convert_excel_to_csv(file_name):
    """Import excel data and export as csv file.
    """
    # import the excel sheet
    df = pd.read_excel(os.path.join(os.path.join(os.getcwd(), "data"), file_name+".xlsx"))

    # export to csv
    df.to_csv(os.path.join(os.path.join(os.getcwd(), "data"), file_name+".csv"))

    return



def replace_missing_data_with_nan(df, verbose=True):
    """Replace -999 as np.nan in dataframe. Need different strategies for different data types
    """
    # iterate across each column
    for column in df:

        # if int data type, first convert to float
        if pd.api.types.is_integer_dtype(df[column]):
            print(column, 'converting to float')
            df[column] = df[column].astype(float)

        # use replace when column has object data type
        if df[column].dtype == object:
            print(column, 'object')
            df = df.replace("-999", np.nan)

        # use np.isclose for numeric columns
        elif df[column].dtype == float:
            print(column, 'float')
            df[column] = df[column].mask(np.isclose(df[column].values, -999.0))
        
        # display number of nan in each column
        if verbose:
            print(column, df[column].isna().sum())

    return df


# def generate_tidy_dataframe_waipara_aws(file_name):


def convert_to_pandas_datetime_waipara_aws():
    a = pd.to_datetime('2023-01-01 0.0', format='%Y-%m-%d %H:%M')
    print(a)




def generate_relevant_utc_list(utc, past_min, past_max):

    # initialise list of utc values to extract
    list_of_utc = []

    # generate list of UTC values to use for 
    for i in range(past_min, past_max+1):
        list_of_utc.append(utc - i*100)

    # return list of utc times
    return list_of_utc



# file_name = "Waipara_AWS_2023"
# convert_excel_to_csv("Waipara_West_2023")


# # import raw data file
# if is_csv:
#     df_raw = pd.read_csv(os.path.join(os.path.join(os.getcwd(), "data"), data_file_name))
# elif is_excel:
#     df_raw = pd.read_excel(os.path.join(os.path.join(os.getcwd(), "data"), data_file_name))

# # show head
# print(df_raw.head())

# # show columns
# print(df_raw.columns)

# a = 1

# # call function to replace missing data with nan
# df_tidy = replace_missing_data_with_nan(df_raw)

# # generate list of utc times to extract
# list_of_utc = generate_relevant_utc_list(utc, 2, 12)
# for u in list_of_utc:
#     a = df_tidy.loc[(df_tidy['DateTime(UTC)'] == u) & (df_tidy['Location'] == location)]
#     b= a['DateTime(UTC)']
#     print(f'{b:.9f}')


# # # display station names in alphabetical order
# # print(np.sort(data_tidy['Location'].unique()))
# # a = data_tidy.loc[(data_tidy['DateTime(UTC)'] == 202402150100) & (data_tidy['Location'] == 'NZWB')]
# # print(df_tidy.head())
# # print(df_tidy.tail())