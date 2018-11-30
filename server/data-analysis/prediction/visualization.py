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