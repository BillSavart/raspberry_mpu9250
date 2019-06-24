import matplotlib.pyplot as plt
import numpy as np

std_stop = []
std_walk = []
i = 1
while i <= 100:
	stop_f = "./data/test_stop"+str(i)+".txt"
	walk_f = "./data/test_walk"+str(i)+".txt"
	std_stop.append(np.std(np.loadtxt(stop_f)))
	std_walk.append(np.std(np.loadtxt(walk_f)))
	i = i + 1

const_x = np.zeros(100)
plt.plot(const_x,std_stop,'.')
plt.plot(const_x,std_walk,'*')
plt.show()
