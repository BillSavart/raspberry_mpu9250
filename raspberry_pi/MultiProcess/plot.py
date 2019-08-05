import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
count = 1

plt.figure(1)
temp = 0
while count <= 98:
    stop_f = np.loadtxt("left_waist.txt")
    walk_f = np.loadtxt("no_turn_waist.txt")
    run_f = np.loadtxt("right_waist.txt")

    #y_stop = signal.lfilter(b,a,stop_f)
    #y_walk = signal.lfilter(b,a,walk_f)
    #y_run = signal.lfilter(b,a,run_f)

    #std_s = np.std(y_stop)
    #std_w = np.std(y_walk)
    #std_r = np.std(y_run)
    tmp = []
    tmp_walk = []
    tmp_run = []
    while temp < 500:
        tmp.append(stop_f[temp*count])
        tmp_walk.append(walk_f[temp*count])
        tmp_run.append(run_f[temp*count])
        std_s = np.std(tmp)
        std_w = np.std(tmp_walk)
        std_r = np.std(tmp_run)
  #      print(temp)
        temp = temp + 1

    plt.scatter(std_s, 0, color='blue')
    plt.scatter(std_w, 0, color='red')
    plt.scatter(std_r, 0, color='green')

    count = count + 1
    temp = 0
    print(count)
plt.show()
