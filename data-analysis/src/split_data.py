# Importing the libraries
import csv
import os
import pandas as pd

# Importing the raw dataset
filedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data'))
filepath = os.path.join(filedir, 'sensor_data.csv')
data = pd.read_csv(filepath)

# Transforming type of data
data['Timestamp'] = pd.to_datetime(data['Timestamp'])

# Deleting outlier
data = data[data['Temperature'] <= 50]
data = data[data['Temperature'] > -50]
data = data[data['Temperature'] <= 100]
data = data[data['Temperature'] >= 0]

group = data.groupby(data['Timestamp'].dt.date)

for k, v in group:
  v.loc[:, 'Timestamp'] = v.loc[:, 'Timestamp'].dt.hour * 3600 + v.loc[:, 'Timestamp'].dt.minute * 60 + v.loc[:, 'Timestamp'].dt.second
  v.to_csv(os.path.join(filedir, str(k) + '.csv'), index = False)