from pandas.core.common import flatten

from .extract_data import extracting_pollutants_data


######################### creating a list of 168 values containing last 24 hrs data of 7 pollutants to feed in the aqi predicter
def create_aqi_input_sample(from_date, to_date, state, city, criteria, station_id, p_id, parameters, station_name):
    parameters, pollutants_data = extracting_pollutants_data(from_date, to_date, state, city, criteria, station_id, p_id, parameters, station_name)
    # print(pollutants_data)

    ## creating list of each pollutants data
    pm25 = []; pm10 = [];  NO2 = []; NH3 = []; SO2 = []; CO = []; Ozone = []
    for i in range(len(pollutants_data)):
        pm25.append(list(pollutants_data.values())[i][0])
        pm10.append(list(pollutants_data.values())[i][1])
        NO2.append(list(pollutants_data.values())[i][2])
        NH3.append(list(pollutants_data.values())[i][3])
        SO2.append(list(pollutants_data.values())[i][4])
        CO.append(list(pollutants_data.values())[i][5])
        Ozone.append(list(pollutants_data.values())[i][6])

    return list(flatten(pollutants_data.values())), [pm25, pm10, NO2, NH3, SO2, CO, Ozone]



##calling fn
# aqi_sample_data = create_aqi_input_sample()
# print(aqi_sample_data)
# print(len(aqi_sample_data))

