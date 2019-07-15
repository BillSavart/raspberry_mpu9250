import matplotlib.pyplot as plt
import numpy as np

count = 1

plt.figure(1)

while count <= 100:
    stop_f = np.loadtxt("stop" + str(count) + ".txt")
    walk_f = np.loadtxt("walk" + str(count) + ".txt")
    run_f = np.loadtxt("run" + str(count) + ".txt")

    std_s = np.std(stop_f)
    std_w = np.std(walk_f)
    std_r = np.std(run_f)

    plt.scatter(std_s, 0, color='blue')
    plt.scatter(std_w, 0, color='red')
    plt.scatter(std_r, 0, color='green')

    count = count + 1
plt.show()