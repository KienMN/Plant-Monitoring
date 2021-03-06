"""
Predicting pumping time base on soil moisture value
"""

# Importing the libraries
import time
from pymongo import MongoClient
import numpy as np
import pandas as pd
from sklearn.externals import joblib
from keras.models import load_model
import os

# Scheduler
s = sched.scheduler(time.time, time.sleep)

# Date and time for first prediction time
start_date = time.strftime("%Y-%m-%d", time.localtime())
start_time = '07:00:00'

# Active prediction time
active_time_string = start_date + " " + start_time
ts = time.strptime(active_time_string, "%Y-%m-%d %H:%M:%S")
active_time_seconds = time.mktime(ts)

# Sampling pace measured by seconds
sampling_pace = 5

# Model file path
regressor_path = os.path.join(os.path.dirname(__file__), "../models/model_rnn_1.h5") 
scaler_path = os.path.join(os.path.dirname(__file__), "../models/scaler_rnn_1.sav")
classifier_path = os.path.join(os.path.dirname(__file__), "../models/classifier_1.sav")

# RNN timesteps
rnn_timesteps = 60

# Getting the dataset
def get_dataset_from_database(number_of_records = 0):
  mongo_client = MongoClient('localhost', 27017)
  db = mongo_client.plant_monitoring
  collection = db.sensor_data
  data = collection.find().skip(collection.count() - number_of_records)
  dataset = []
  for record in data:
    dataset.append(record.get('SoilMoisture'))
  dataset = np.array(dataset).reshape(-1, 1)
  mongo_client.close()
  return dataset

def predict_soil_moisture_values(historical_values, future_minutes):
  # Number of future records
  future_records = future_minutes * 60 // sampling_pace

  # Feature scaling
  sc = joblib.load(scaler_path)
  inputs = sc.transform(historical_values)
  
  # Prediction result
  prediction = []
  
  # Preparing dataset for prediction
  X_test = []
  n_samples = len(historical_values)
  for i in range (rnn_timesteps, n_samples):
    X_test.append(inputs[i - rnn_timesteps: i, :])
  X_test = np.array(X_test)
  X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

  # Loading regressor model
  regressor = load_model(regressor_path)

  # Predicting the result
  predicted_values = regressor.predict(X_test)
  prediction.append(predicted_values[- 1, :].copy())

  # Predicting the result for future time
  while (len(prediction) < future_records):
    new_input = []
    for i in range (1, rnn_timesteps):
      new_input.append(X_test[-1, i, :])
    new_input.append(predicted_values[-1, :])
    new_input = np.array(new_input)
    new_input = np.reshape(new_input, (1, new_input.shape[0], new_input.shape[1]))
    X_test = np.append(X_test[1:, :, :], new_input, axis = 0)
    predicted_values = regressor.predict(X_test)
    prediction.append(predicted_values[- 1, :].copy())
  
  prediction = np.array(prediction)
  prediction = prediction.reshape((-1, 1))
  prediction = sc.inverse_transform(prediction)
  return prediction

def predict_soil_moisture_from_database(activate_time_seconds, records_from_present = 1080, future_minutes = 30):
  # Getting historical data
  historical_values = get_dataset_from_database(records_from_present)

  # Predicting future values
  predicted_values = predict_soil_moisture_values(historical_values, future_minutes)
  
  # Saving to the database
  mongo_client = MongoClient('localhost', 27017)
  db = mongo_client.plant_monitoring
  collection = db.soilmoisture_prediction
  n_samples = len(predicted_values)
  for i in range (n_samples):
    future_time = activate_time_seconds + (i + 1) * sampling_pace
    record = {
      "PredictionTime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(activate_time_seconds)),
      "FutureTime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(future_time)),
      "PredictedSoilMoisture": predicted_values.item(i)
    }
    collection.insert_one(record)
  mongo_client.close()

def predict_soil_moisture_from_csvfile(input_filepath, output_filepath, future_minutes = 30):
  # Getting historical data
  historical_values = pd.read_csv(input_filepath, header = None).values

  # Predicting future values
  predicted_values = predict_soil_moisture_values(historical_values, future_minutes)
  
  # Saving to the csvfile
  predicted_values = pd.DataFrame(predicted_values)
  predicted_values.to_csv(output_filepath, index = False, header = False)