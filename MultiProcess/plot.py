import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
count = 1

plt.figure(1)
temp = 0
while count <= 100:
    stop_f = np.loadtxt("stop.txt")
    walk_f = np.loadtxt("walk.txt")
    #run_f = np.loadtxt("run" + str(count) + ".txt")

    #y_stop = signal.lfilter(b,a,stop_f)
    #y_walk = signal.lfilter(b,a,walk_f)
    #y_run = signal.lfilter(b,a,run_f)

    #std_s = np.std(y_stop)
    #std_w = np.std(y_walk)
    #std_r = np.std(y_run)
    tmp = []
    tmp_walk = []
    while temp < 500:
        tmp.append(stop_f[temp])
        tmp_walk.append(walk_f[temp])
        std_s = np.std(tmp)
        std_w = np.std(tmp_walk)
        print(temp)
        temp = temp + 1

    plt.scatter(std_s, 0, color='blue')
    plt.scatter(std_w, 0, color='red')
    #plt.scatter(std_r, 0, color='green')

    count = count + 1
    temp = 0
    print(count)
plt.show()