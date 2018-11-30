# Training random forest classifier

# Importing the libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Importing training dataset
X_train = []
y_train = []

dataset = pd.read_csv('data/2018-11-13.csv')
dataset_train = dataset.iloc[5774: 5804, [3, 5]].values

for i in range (1, 30):
    X_train.append(dataset_train[i - 1: i + 1, 0])
    y_train.append(np.amax(dataset_train[i - 1: i + 1, 1]))
    
dataset = pd.read_csv('data/2018-11-16.csv')
dataset_train = dataset.iloc[6898: 6928, [3, 5]].values

for i in range (1, 30):
    X_train.append(dataset_train[i - 1: i + 1, 0])
    y_train.append(np.amax(dataset_train[i - 1: i + 1, 1]))
    
dataset = pd.read_csv('data/2018-11-18.csv')
dataset_train = dataset.iloc[7594: 7624, [3, 5]].values

for i in range (1, 30):
    X_train.append(dataset_train[i - 1: i + 1, 0])
    y_train.append(np.amax(dataset_train[i - 1: i + 1, 1]))

X_train = np.array(X_train)
y_train = np.array(y_train)

# Visualizing training dataset
colors = ['red', 'blue']
for i in np.unique(y_train):
    plt.scatter(X_train[np.where(y_train == i)[0], 0],
                X_train[np.where(y_train == i)[0], 1],
                color = colors[i], label = 'Class' + str(i))
plt.legend()
plt.show()

# Creating classifier model
from sklearn.ensemble import RandomForestClassifier
classifier = RandomForestClassifier(n_estimators = 4, criterion = 'entropy', random_state = 0)

# Training the model
classifier.fit(X_train, y_train)

# Predicting the model
y_pred = classifier.predict(X_train)

# Confusion matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_train, y_pred)

# Dumping the model
from sklearn.externals import joblib
joblib.dump(classifier, 'models/classifier_1.sav')

# Importing the test dataset
dataset_test = pd.read_csv('predict_2_result.csv', header = None).values
n_samples = len(dataset_test)
X_test = []
for i in range (1, n_samples):
    X_test.append(dataset_test[i - 1: i + 1, 0])
X_test = np.array(X_test)

# Predicting the result
y_pred = classifier.predict(X_test)

# Visualizing the result
plt.plot(dataset_test, color = 'blue', label = 'Predicted soil moisture')
plt.scatter(np.where(y_pred == 1)[0], dataset_test[np.where(y_pred == 1)[0]], color = 'red', label = 'Pumping point')
plt.show()

X_set, y_set = X_train, y_train
X1, X2 = np.meshgrid(np.arange(X_train[:, 0].min() - 1, X_train[:, 0].max() + 1, step = 0.01),
                     np.arange(X_train[:, 1].min() - 1, X_train[:, 1].max() + 1, step = 0.01))
from matplotlib.colors import ListedColormap
plt.contourf(X1, X2, classifier.predict(np.array([X1.ravel(), X2.ravel()]).T).reshape(X1.shape),
             alpha = 0.75, cmap = ListedColormap(('red', 'green')))
plt.xlim(X1.min(), X1.max())
plt.ylim(X2.min(), X2.max())
for i, j in enumerate (np.unique(y_set)):
    plt.scatter(X_set[y_set == j, 0], X_set[y_set == j, 1],
                c = ListedColormap(('red', 'green'))(i), label = j)
plt.title('Classification (Training set)')
plt.xlabel('Former value')
plt.ylabel('Latter value')
plt.legend()
plt.show()