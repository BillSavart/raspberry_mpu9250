import tensorflow as tf
import numpy as np
import pandas as pd
from sklearn import ensemble, preprocessing, metrics
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

stop_data = np.loadtxt('test_data/stopfilt.txt')
walk_data = np.loadtxt('test_data/walkfilt.txt')

#linspace
stop_y = np.loadtxt('test_data/stop_y.txt')
walk_y = np.loadtxt('test_data/walk_y.txt')

data_x = np.append(stop_data, walk_data)
data_y = np.append(stop_y, walk_y)

data_x = []
data_y = []

test_x = []

i = 0
for stop in stop_data:
	if i > 50:
		data_x.append([stop, stop_y[i]])
		data_y.append(1)
	else:
		test_x.append([stop, stop_y[i]])
	i = i + 1

i = 0

for walk in walk_data:
	if i > 50:
		data_x.append([walk, walk_y[i]])
		data_y.append(2)
	else:
		test_x.append([walk, walk_y[i]])
	i = i + 1

#建立模型
forest = ensemble.RandomForestClassifier(n_estimators = 100)
forest_fit = forest.fit(data_x, data_y)

i = 0
correct = 0
test_y_predicted = forest.predict(test_x)

for x in test_y_predicted:
	if x == data_y[i]:
		correct = correct + 1
	i = i + 1

print(correct)
