import pandas as pd

# from extract_data import extracting_pollutants_data

# parameters, pollutants_data = extracting_pollutants_data()

################################ creating data to add into the database
def create_data_to_update_database(polls_data):
    data = pd.DataFrame(list(polls_data.values()))

    ## removing nan values
    data.dropna(inplace = True)

    #resetting index
    data.reset_index(drop=True, inplace=True)

    # ## renaming columns
    # data.columns=[0,1,2,3,4,5,6]

    return data

# data_to_update_database = create_data_to_update_database(pollutants_data)
# print(len(data_to_update_database))
# print(data_to_update_database)
# print(pd.DataFrame(data_to_update_database).shape)
# print(pd.DataFrame(data_to_update_database).head())
