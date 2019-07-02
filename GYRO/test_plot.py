import matplotlib.pyplot as plt
import numpy as np

const_x = np.zeros(100)
plt.figure(1)
std_stop = []
std_walk = []
i = 1
while i <= 100:
	stop_f = "./turning_data/no_turn"+str(i)+".txt"
	std_stop.append(np.loadtxt(stop_f))
	i = i + 1
for unit in std_stop:
	std_walk.append(np.std(unit))

const_x = np.zeros(100)
plt.scatter(const_x,std_walk,'.')
plt.show()
