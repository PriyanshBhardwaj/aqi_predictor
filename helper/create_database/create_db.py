import pandas as pd
import numpy as np
import os

## loading datasets
# cwd = os.getcwd()
df_2020 = pd.read_csv("../../data/Raw_data_1Hr_2020_site_5345_Sector-51_Gurugram_HSPCB_1Hr.csv")
df_2021 = pd.read_csv("../../data/Raw_data_1Hr_2021_site_5345_Sector-51_Gurugram_HSPCB_1Hr.csv")
df_2022 = pd.read_csv("../../data/Raw_data_1Hr_2022_site_5345_Sector-51_Gurugram_HSPCB_1Hr.csv")
df_2023 = pd.read_csv("../../data/Raw_data_1Hr_2023_site_5345_Sector-51_Gurugram_HSPCB_1Hr.csv")
df_2024 = pd.read_csv("../../data/Raw_data_1Hr_2024_site_5345_Sector-51_Gurugram_HSPCB_1Hr.csv")

## creating pollutants dataset

pollutants_2020 = pd.DataFrame(df_2020[['PM2.5 (µg/m³)', 'PM10 (µg/m³)', 'NO2 (µg/m³)', 'NH3 (µg/m³)', 'SO2 (µg/m³)', 'CO (mg/m³)', 'Ozone (µg/m³)']])
pollutants_2021 = pd.DataFrame(df_2021[['PM2.5 (µg/m³)', 'PM10 (µg/m³)', 'NO2 (µg/m³)', 'NH3 (µg/m³)', 'SO2 (µg/m³)', 'CO (mg/m³)', 'Ozone (µg/m³)']])
pollutants_2022 = pd.DataFrame(df_2022[['PM2.5 (µg/m³)', 'PM10 (µg/m³)', 'NO2 (µg/m³)', 'NH3 (µg/m³)', 'SO2 (µg/m³)', 'CO (mg/m³)', 'Ozone (µg/m³)']])
pollutants_2023 = pd.DataFrame(df_2023[['PM2.5 (µg/m³)', 'PM10 (µg/m³)', 'NO2 (µg/m³)', 'NH3 (µg/m³)', 'SO2 (µg/m³)', 'CO (mg/m³)', 'Ozone (µg/m³)']])
pollutants_2024 = pd.DataFrame(df_2024[['PM2.5', 'PM10', 'NO2', 'NH3', 'SO2', 'CO', 'Ozone']])

#renaming pollutants_2024 column names to match others
pollutants_2024.columns = ['PM2.5 (µg/m³)', 'PM10 (µg/m³)', 'NO2 (µg/m³)', 'NH3 (µg/m³)', 'SO2 (µg/m³)', 'CO (mg/m³)', 'Ozone (µg/m³)']


## since pollutants_2024 data is in string, converting it to float
# and replacing None values to NaN so that it can be removed later and doesnt cause any discripency in the model

pollutants_2024.replace('None', 'NaN', inplace=True)
pollutants_2024 = pollutants_2024.astype(float)

## concating the pollutants data to create final dataset
pollutants = pd.concat([pollutants_2020, pollutants_2021, pollutants_2022, pollutants_2023, pollutants_2024], axis=0)

## resetting index
pollutants.reset_index(drop=True, inplace=True)

## removing nan values
pollutants.dropna(inplace = True)

#resetting index
pollutants.reset_index(drop=True, inplace=True)

## renaming columns
pollutants.columns=[0,1,2,3,4,5,6]

print(pollutants.shape)
print('\n\n', pollutants.head())

##creating database which will be used to create training data to train the model
pollutants.to_csv('../../database/database.csv', index=False)


# ##loading the dataset
# df = pd.read_csv('/Users/divyansh/Desktop/nlp_tut/AQI_Project/database/database.csv')
# print(df.shape)
# print(df.head())



# data3 = pd.read_csv('../../database/database.csv')
# print(data3.shape)
# print(data3.head())