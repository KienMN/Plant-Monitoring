# Importing the libraries
import sched, time
from pymongo import MongoClient
import numpy as np
import pandas as pd
from sklearn.externals import joblib
import os

# Sampling pace measured by seconds
sampling_pace = 5

# Model file path
classifier_path = os.path.join(os.path.dirname(__file__), "../models/classifier_1.sav")

# Getting the dataset
def get_predicted_soilmoisture_from_database(number_of_records = 0):
  mongo_client = MongoClient('localhost', 27017)
  db = mongo_client.plant_monitoring
  collection = db.soilmoisture_prediction
  data = collection.find().skip(collection.count() - number_of_records)
  dataset = []
  for record in data:
    dataset.append(record.get('PredictedSoilMoisture'))
  dataset = np.array(dataset).reshape(-1, 1)
  return dataset

def predict_pumping_time(predicted_soilmoisture_values):
  # Loading the trained model
  classifier = joblib.load(classifier_path)

  # Preparing dataset for prediction
  n_samples = len(predicted_soilmoisture_values)
  X_test = []
  for i in range (1, n_samples):
    X_test.append(predicted_soilmoisture_values[i - 1: i + 1, 0])
  X_test = np.array(X_test)

  # Predicting the result
  y_pred = classifier.predict(X_test)

  # Pumping period
  pumping_point_index = -1
  period = -1
  points = np.where(y_pred == 1)[0]
  if len(points) != 0:
    pumping_point_index = points[0]
    period = 1
    for i in range (1, len(points)):
      if points[i] - points[i - 1] == 1:
        period += 1
      else:
        break
  return (pumping_point_index, period)

def predict_pumping_time_from_database(activate_time_seconds, future_minutes = 30):
  # Number of future records
  future_records = future_minutes * 60 // sampling_pace

  # Getting predicted moisture values from database
  dataset = get_predicted_soilmoisture_from_database(future_records)

  # Predciting time
  pumping_point_index, period = predict_pumping_time(dataset)

  # Saving to the database
  mongo_client = MongoClient('localhost', 27017)
  db = mongo_client.plant_monitoring
  collection = db.pumping_time_prediction
  predicted_pumping_time = activate_time_seconds + (pumping_point_index + 1) * sampling_pace
  record = {
    "PredictionTime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(activate_time_seconds)),
    "PredictedPumpingTime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(predicted_pumping_time)),
    "Duration": period * sampling_pace
  }
  collection.insert_one(record)
  mongo_client.close()

# output_filepath = os.path.join(os.path.dirname(__file__), '../data/output_demo.csv')
# dataset_test = pd.read_csv(output_filepath, header = None).values
# print(predict_pumping_time(dataset_test))

def predict_pumping_time_from_csv(input_filepath, output_filepath):
  # Getting predicted data
  predicted_values = pd.read_csv(input_filepath, header = None).values

  # Predicting future time
  pumping_point_index, period = predict_pumping_time(predicted_values)
  
  # Saving to the csvfile
  predicted_values = pd.DataFrame(predicted_values)
  predicted_values.to_csv(output_filepath, index = False, header = False)