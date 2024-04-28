## it will take the updated dataset and then retrain the model and if the model's accuracy is greater then before it will save the model.
import pickle
import pandas as pd

from create_train_dataset import create_training_data
from model import train_model, calculate_accuracy, current_threshold, save_model


## creating input and output dataset(list) for training the model
print('creating training data')
input, output = create_training_data('../../database/database.csv')

# 80, 20 split for X_train, X_test          int(len(input)*0.8)
X_train = input[:int(len(input)*0.8)]
X_test = input[int(len(input)*0.8):]

# 80, 20 split for y_train, y_test
y_train = output[:int(len(output)*0.8)]
y_test = output[int(len(output)*0.8):]

## loading model
print('loading current model')
model = pickle.load(open('../../model/polls_xgb.pkl', "rb"))

## retraining the model
print('retraining the model')
new_model, y_preds_df, y_test_df = train_model(model, X_train, y_train, X_test, y_test)

## calculating accuracy
print('calculating new model accuracy')
r2, mae = calculate_accuracy(y_test_df, y_preds_df)

print('r2: ',r2, 'mae: ',mae, '\n',sep='\n')

## checking threshold
print('checking threshold')
passed_threshold = current_threshold(r2, mae)

## saving the model if passed threshold
if passed_threshold:
    print('passed threshold, saving the model')
    save_model(new_model)

else:
    print('threshold not passed')
