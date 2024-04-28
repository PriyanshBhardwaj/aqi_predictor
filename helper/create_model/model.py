import pandas as pd
import numpy as np
import os
from sklearn.metrics import mean_absolute_error, r2_score
import pickle


from create_train_dataset import create_training_data

#supervised ml

# XG Boost using pollutants data
# it will predict next hour pollutants data using last 24 hrs data

def create_model():
    '''load the training dataset and then create the model'''
    ## load dataset
    # '/Users/divyansh/Desktop/nlp_tut/AQI_Project/database/database.csv'
    # data = pd.read_csv('../../database/database.csv')
    input, output = create_training_data('../../database/database.csv')

    # 80, 20 split for X_train, X_test          int(len(input)*0.8)
    X_train = input[:int(len(input)*0.8)]
    X_test = input[int(len(input)*0.8):]

    # 80, 20 split for y_train, y_test
    y_train = output[:int(len(input)*0.8)]
    y_test = output[int(len(input)*0.8):]

    ## creating the model
    my_polls_xgb = xgb.XGBRegressor(n_estimators=1000, max_depth=100, gamma=0.1)
    #these hyperparams values gives best model for now


    return my_polls_xgb, X_train, y_train, X_test, y_test



def train_model(model, X_train, y_train, X_test, y_test):
    '''trains the model'''
    # fit the model
    model.fit(X_train, y_train)

    # predict on the same period
    y_preds = model.predict(X_test)

    # print(y_preds[:4])

    # print(len(y_preds), len(y_test), sep='\n')

    #creating pred df
    y_preds_df = pd.DataFrame(y_preds)
    y_test_df = pd.DataFrame(y_test)

    # print(y_preds_df.head())
    # print(y_test_df.head())

    return model, y_preds_df, y_test_df



def calculate_accuracy(test_df, preds_df):
    ''' calculates model's accuracy '''

    ##calculating accuracy
    r2_poll = {}
    mae_poll = {}

    for i in range(preds_df.shape[1]):
        # print(i)
        r2_poll[i] = r2_score(test_df[i], preds_df[i])
        # new_r2_poll

        mae_poll[i] = mean_absolute_error(test_df[i], preds_df[i])
        # new_mae_poll

        # print(r2_poll, mae_poll, sep='\n')

    r2 = list(r2_poll.values())
    mae = list(mae_poll.values())
    
    return r2, mae


def current_threshold(new_r2: list, new_mae: list):
    ''' checks new r2 and mae and if it passess the threshold value then return true otherwise false '''
    threshold = pd.read_csv('./threshold.csv')

    curr_r2 = list(threshold.iloc[0])
    curr_mae = list(threshold.iloc[1])

    r2_count = 0
    mae_count = 0

    for i in range(len(curr_r2)):
        if new_r2[i] > curr_r2[i]: r2_count+=1
        if new_mae[i] < curr_mae[i] : mae_count+=1
    
    print('\n\n', 'r2_count: ', r2_count, 'mae_count: ', mae_count)
    
    if r2_count or mae_count >= 4:
        curr_r2 = new_r2
        curr_mae = new_mae

        threshold_data = [curr_r2, curr_mae]

        threshold = pd.DataFrame(threshold_data)
        threshold.to_csv('threshold.csv', index=False)

        return True
    
    return False




def save_model(model):
    '''saves the model'''
    file_name = "polls_xgb1.pkl"
    # save
    pickle.dump(model, open("../../model/"+file_name, "wb"))


    # # load & predict
    # xgb_model_loaded = pickle.load(open('./polls_xgb.pkl', "rb"))
    # xgb_model_loaded.predict([[40.07, 83.13, 23.12, 32.09, 17.59, 0.5, 87.84, 42.11, 77.66, 22.8, 34.99, 18.67, 0.5, 77.24, 42.19, 91.32, 23.99, 37.07, 19.23, 0.52, 54.08, 46.56, 117.94, 26.76, 37.74, 20.43, 0.57, 49.19, 41.26, 89.94, 25.98, 45.65, 20.89, 0.54, 74.2, 29.89, 49.0, 24.82, 49.26, 21.13, 0.49, 67.97, 21.53, 29.13, 24.41, 47.12, 22.1, 0.47, 74.16, 20.47, 21.52, 22.38, 44.92, 22.04, 0.46, 64.41, 20.02, 27.18, 21.74, 44.44, 19.3, 0.46, 57.7, 18.8, 29.41, 24.76, 47.33, 22.6, 0.45, 76.66, 17.06, 31.94, 23.72, 50.21, 23.67, 0.44, 78.14, 16.85, 24.41, 21.24, 49.22, 24.48, 0.43, 69.5, 14.83, 25.48, 21.03, 46.43, 23.43, 0.4, 83.16, 14.43, 21.49, 20.14, 44.29, 22.78, 0.39, 64.78, 13.28, 30.23, 20.08, 46.6, 23.04, 0.4, 48.74, 15.6, 40.22, 20.23, 46.1, 23.39, 0.4, 27.5, 20.39, 34.91, 21.61, 44.11, 23.79, 0.44, 30.51, 25.36, 34.08, 22.03, 38.87, 22.67, 0.46, 49.42, 25.96, 28.38, 23.43, 32.5, 21.48, 0.45, 63.65, 26.85, 39.93, 32.35, 29.65, 5.64, 0.36, 75.54, 24.86, 38.46, 23.82, 36.32, 8.82, 0.37, 79.08, 21.37, 40.84, 22.5, 35.24, 11.72, 0.38, 80.71, 25.53, 57.55, 22.11, 35.46, 13.9, 0.4, 79.74, 27.64, 63.56, 22.66, 31.92, 15.12, 0.44, 68.01], [42.11, 77.66, 22.8, 34.99, 18.67, 0.5, 77.24, 42.19, 91.32, 23.99, 37.07, 19.23, 0.52, 54.08, 46.56, 117.94, 26.76, 37.74, 20.43, 0.57, 49.19, 41.26, 89.94, 25.98, 45.65, 20.89, 0.54, 74.2, 29.89, 49.0, 24.82, 49.26, 21.13, 0.49, 67.97, 21.53, 29.13, 24.41, 47.12, 22.1, 0.47, 74.16, 20.47, 21.52, 22.38, 44.92, 22.04, 0.46, 64.41, 20.02, 27.18, 21.74, 44.44, 19.3, 0.46, 57.7, 18.8, 29.41, 24.76, 47.33, 22.6, 0.45, 76.66, 17.06, 31.94, 23.72, 50.21, 23.67, 0.44, 78.14, 16.85, 24.41, 21.24, 49.22, 24.48, 0.43, 69.5, 14.83, 25.48, 21.03, 46.43, 23.43, 0.4, 83.16, 14.43, 21.49, 20.14, 44.29, 22.78, 0.39, 64.78, 13.28, 30.23, 20.08, 46.6, 23.04, 0.4, 48.74, 15.6, 40.22, 20.23, 46.1, 23.39, 0.4, 27.5, 20.39, 34.91, 21.61, 44.11, 23.79, 0.44, 30.51, 25.36, 34.08, 22.03, 38.87, 22.67, 0.46, 49.42, 25.96, 28.38, 23.43, 32.5, 21.48, 0.45, 63.65, 26.85, 39.93, 32.35, 29.65, 5.64, 0.36, 75.54, 24.86, 38.46, 23.82, 36.32, 8.82, 0.37, 79.08, 21.37, 40.84, 22.5, 35.24, 11.72, 0.38, 80.71, 25.53, 57.55, 22.11, 35.46, 13.9, 0.4, 79.74, 27.64, 63.56, 22.66, 31.92, 15.12, 0.44, 68.01, 29.94, 67.32, 22.59, 34.0, 16.26, 0.44, 62.84]])
    # print(np.array(preds).tolist()[0], '\n\n\n')


# model, preds, test = create_model()
# r2, mae = calculate_accuracy(test, preds)
# save_model(model, 'path_to_model_directory')