# Training RNN model

# Importing the libraries
import numpy as np
import pandas as pd
import os

# Importing the training set
dataset_train = pd.read_csv('data/dataset1.csv')
training_set = dataset_train.iloc[:, :4].values

# Feature scaling
from sklearn.preprocessing import MinMaxScaler
sc = MinMaxScaler()
training_set_scaled = sc.fit_transform(training_set)
from sklearn.externals import joblib
joblib.dump(sc, 'models/scaler_rnn_1.sav')

# Create inputs for RNN
n_samples = len(training_set_scaled)
X_train = []
y_train = []

for i in range (60, n_samples):
  X_train.append(training_set_scaled[i - 60: i, 2: 3])
  y_train.append(training_set_scaled[i, 2])
    
X_train, y_train = np.array(X_train), np.array(y_train)

# Reshape inputs
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

# Building the RNN

# Importing the Keras libraries and packages
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout

# Initialising the RNN
regressor = Sequential()

# Adding the first LSTM layer and some Dropout regularisation
regressor.add(LSTM(units = 50, return_sequences = True, input_shape = (X_train.shape[1], X_train.shape[2])))
regressor.add(Dropout(0.2))

# Adding a second LSTM layer and some Dropout regularisation
regressor.add(LSTM(units = 50, return_sequences = True))
regressor.add(Dropout(0.2))

# Adding a third LSTM layer and some Dropout regularisation
regressor.add(LSTM(units = 50, return_sequences = True))
regressor.add(Dropout(0.2))

# Adding a fourth LSTM layer and some Dropout regularisation
regressor.add(LSTM(units = 50))
regressor.add(Dropout(0.2))

# Adding the output layer
regressor.add(Dense(units = 1))

# Compiling the RNN
regressor.compile(optimizer = 'adam', loss = 'mean_squared_error')

# Fitting the RNN to the Training set
from keras.callbacks import ModelCheckpoint
mc = ModelCheckpoint('models/model_rnn_1-{epoch:03d}.h5', period=50)
regressor.fit(X_train, y_train, epochs = 200, batch_size = 32, callbacks = [mc])

# Saving the RNN
regressor.save("models/model_rnn_1.h5")