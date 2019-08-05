import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

order = 3
Wn = 0.005
b,a = signal.butter(order,Wn,'low')

STOP_FILE_NAME = "../MultiProcess/stop.txt"
WALK_FILE_NAME = "../MultiProcess/walk.txt"
RUN_FILE_NAME = "../MultiProcess/run"
NO_TURN_FILE_NAME = "../MultiProcess/no_turn"
TURN_RIGHT_FILE_NAME = "../MultiProcess/right_turn"
TURN_LEFT_FILE_NAME = "../MultiProcess/left_turn"
ONE_NAME = "../MultiProcess/100walk"
BILL_NAME = "../MultiProcess/billwalk"

stop_data = []
walk_data = []
run_data = []
no_turn_data = []
turn_right_data = []
turn_left_data = []
one_data = []
bill_data =[]

stop_data = np.loadtxt(STOP_FILE_NAME)
walk_data = np.loadtxt(WALK_FILE_NAME)
stop_data = signal.lfilter(b,a,stop_data)
walk_data = signal.lfilter(b,a,walk_data)

cons_no_move_x = range(len(stop_data))
cons_walk_x = range(len(walk_data))
cons_run_x = np.zeros(25)
cons_no_turn_x = np.zeros(31)  
cons_right_turn_x = np.zeros(32)  
cons_left_turn_x = np.zeros(33)  
cons_100_x = np.zeros(5)
cons_bill_x = np.zeros(6)

print(len(stop_data))

plt.figure(num =1)
plt.scatter(cons_walk_x,walk_data,label = "walk")
plt.scatter(cons_no_move_x,stop_data,label = "stop")
#plt.scatter(cons_run_x,run_std,label = "run")
#plt.scatter(cons_no_turn_x,no_turn_std,label = "no turn")
#plt.scatter(cons_right_turn_x,turn_right_std,label = "turn_right")
#plt.scatter(cons_left_turn_x,turn_left_std,label = "turn_left")
#plt.scatter(cons_100_x,one_std,label = "100")
#plt.scatter(cons_bill_x,bill_std,label = "bill")
plt.legend(loc= "upper right")
plt.show()

