# Creating the required dataset of (1, 168) for input and (1,7) for output

# input: 1 sample having size (1, 168) represting 24 hrs data for 7 pollutants => 24*7 = 168
# (24,7)
# (24,7)
# ......
# ......
# ......*31909            31933 - 24 = 31909

# output: 1 sample having size (1,7) representing next hr, that is, 25th hr pollutants data
# (1,7)
# (1,7)
# ......
# ......
# ......*31909            31933 - 24 = 31909

# the input and output data both will be a list because it is giving good results
# input shape => 31909*1*168
# output shape => 31909*1*7

import pandas as pd
import numpy as np
import os
from pandas.core.common import flatten

def create_training_data(pollutants_dataset: str):
    '''
        this function will create two datasets(list) input & output as mentioned above and return them
    '''
    pollutants = pd.read_csv(pollutants_dataset)

    ### creating input: a list of n samples and each sample having shape 1*168
    input = []
    for i in range(len(pollutants)-24):
        data_entry = []
        for j in range(24):
            data_entry.append(list(pollutants.iloc[i+j]))
        data_entry = list(flatten(data_entry))
        # print(data_entry)
        # break
        input.append(data_entry)
        # if i ==1: break
    # print(len(input))
    # print(input)


    ### Creating output: a list of n samples and each sample having size 1*7
    output = []
    for i in range(24, len(pollutants)):
        output.append(list(pollutants.iloc[i]))
        # if i==25: break
    # print(len(output))
    # print(output)

    return input, output


# input, output = create_training_data('/Users/divyansh/Desktop/nlp_tut/AQI_Project/database/database.csv')