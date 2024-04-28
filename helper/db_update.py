import pandas as pd
from datetime import datetime

from extract_data import extracting_pollutants_data
from data_for_updating_db import create_data_to_update_database

# from data_extracter import extract_data



def updating_db():
    ##read database
    data = pd.read_csv('../database/database.csv')
    # print(data.shape, '\n\n')
    # print(data.head())

    ## last date_time in db
    last_date_in_db = open("last_date_in_db.txt", "r")
    # print(f.read())

    ##current date_time
    current_date_time = datetime.now().strftime("%d-%m-%Y T%H:%M:%SZ")
    # print((current_date_time))

    ## updating the date stored
    f = open("last_date_in_db.txt", "w")
    f.write(current_date_time)
    f.close()

    parameters, pollutants_data = extracting_pollutants_data(from_date = last_date_in_db, to_date = current_date_time, state = 'Haryana', city = 'Gurugram', criteria = '1 Hours', station_id = 'site_5345', p_id = ['parameter_193', 'parameter_215', 'parameter_194', 'parameter_311', "parameter_312", "parameter_203", "parameter_222"], parameters = ['PM2.5', 'PM10', 'NO2', 'NH3', 'SO2', 'CO', 'Ozone'], station_name='Sector-51, Gurugram - HSPCB')

    data_for_update_df = create_data_to_update_database(pollutants_data)

    data_for_update_df.columns = data.columns

    # data_for_update_df = pd.DataFrame(data_for_update)

    # print(data_for_update_df.shape, '\n\n')
    # print(data_for_update_df.head(), '\n\n')

    # data_for_update_df.to_csv('test.csv', index=False)

    # concating both datasets
    data = pd.concat([data, data_for_update_df], axis=0, ignore_index=True)

    #resetting index
    data.reset_index(drop=True, inplace=True)

    data.to_csv('../database/database.csv', index=False)

    # print(data.shape)
    # print(data.head())
    # print(data.tail())

updating_db()