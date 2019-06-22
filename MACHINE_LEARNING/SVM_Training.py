import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

stop_data = np.loadtxt('stopfilt.txt')
walk_data = np.loadtxt('walkfilt.txt')

stop_y = np.loadtxt('stop_y.txt')
walk_y = np.loadtxt('walk_y.txt')

data_x = np.append(stop_data, walk_data)
data_y = np.append(stop_y, walk_y)

