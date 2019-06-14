import tensorflow as tf
import numpy as np
from scipy import signal

#turn off the warning messages by compiler
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Read in data
stop_data = np.loadtxt("../GYRO/stop.txt")
stop_time = np.loadtxt("../GYRO/stop_time.txt")

walk_data = np.loadtxt("../GYRO/walk.txt")
walk_time = np.loadtxt("../GYRO/walk_time.txt")

#filter
order = 3
Wn = 0.003
b,a = signal.butter(order, Wn , 'low')

temp_data = np.append(stop_data, walk_data)
temp_time = np.append(stop_time, walk_time)

# The rest of the part
stop_data_length = len(stop_data)
walk_data_length = len(walk_data)

y_data = np.zeros(stop_data_length)
walk_y_data = np.zeros(walk_data_length) 
walk_y_data[:] = 0.4
y_data = np.append(y_data, walk_y_data)

Weights = tf.Variable(tf.random_uniform([1],-5.0,5.0))
biases = tf.Variable(tf.zeros([1]))

temp_data = signal.lfilter(b, a, temp_data)

# at^2
y = (abs(temp_data) * temp_time * temp_time) * Weights + biases

loss = tf.reduce_mean(tf.square(y - y_data))

optimizer = tf.train.GradientDescentOptimizer(0.5)  #learning rate
train = optimizer.minimize(loss)
init = tf.initialize_all_variables()

sess = tf.Session()
sess.run(init)     #Very important

train_count = 10000

for step in range(train_count):
	sess.run(train)
	print(step,sess.run(Weights),sess.run(biases),sess.run(loss))
