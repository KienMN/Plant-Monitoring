# Importing the libraries
import os
import pandas as pd
import matplotlib.pyplot as plt


# Importing the dataset
filedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data'))

plt.figure(figsize=(12,8))
colors = ['red', 'green', 'blue', 'yellow', 'cyan']

for i in [13, 16, 18, 21]:
  filepath = os.path.join(filedir, '2018-11-' + str(i) + '.csv')
  data = pd.read_csv(filepath)

  # Setting co-ordinates
  value = data.loc[3960: 8640, 'SoilMoisture'].values

  for j in range (1, len(value)):
    if value[j] < 10:
      value[j] = value[j - 1]
    elif value[j] < 20:
      value[j] = value[j] * 2

  # Visualizing
  plt.plot(value, c = colors[i % len(colors)])

plt.show()

# # Importing the raw dataset
# filedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data'))
# filepath = os.path.join(filedir, 'sensor_data.csv')
# data = pd.read_csv(filepath)

# Transforming type of data
# data['Timestamp'] = pd.to_datetime(data['Timestamp'])

# Deleting outlier
# data = data[data['Temperature'] <= 50]
# data = data[data['Temperature'] > -50]
# data = data[data['Temperature'] <= 100]
# data = data[data['Temperature'] >= 0]

# # Setting co-ordinates
# x = data.loc[:, 'Temperature']
# y = data.loc[:, 'SoilMoisture']
# z = data.loc[:, 'PumpingStatus']

# # Visualizing
# print(data[z == 1])
# plt.figure(figsize=(12,8))
# plt.scatter(x[z != 1], y[z != 1], c = 'red')
# plt.show()