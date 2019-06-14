import tensorflow as tf
import numpy as np
from scipy import signal

#turn off the warning messages by compiler
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

x_data = np.random.rand(1000)

y_data = 3.1415*3.1415*x_data+2.6789*3.1415

Weights = tf.Variable(tf.random_uniform([1],-5,5))
biases = tf.Variable(tf.zeros([1]))


# at^2
y = x_data * Weights * Weights + biases*Weights

loss = tf.reduce_mean(tf.square(y - y_data))

optimizer = tf.train.GradientDescentOptimizer(0.5)  #learning rate
train = optimizer.minimize(loss)
init = tf.initialize_all_variables()

sess = tf.Session()
sess.run(init)     #Very important

train_count = 1000

for step in range(train_count):
	sess.run(train)
	print(step,sess.run(Weights),sess.run(biases),sess.run(loss))
