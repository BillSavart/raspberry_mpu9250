import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

order = 3
Wn = 0.9
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

stop_std = []
walk_std = []
run_std = []
no_turn_std = []
turn_right_std = []
turn_left_std = []
one_std = []
bill_std = []

stop_median = []
walk_median = []
run_median = []
no_turn_median = []
turn_right_median = []
turn_left_median = []
one_median = []
bill_median = []

stop_average = []
walk_average = []
run_average = []
no_turn_average = []
turn_right_average = []
turn_left_average = []
one_average = []
bill_average = []

cons_no_move_x = np.zeros(32)
cons_walk_x = np.zeros(35)
cons_run_x = np.zeros(25)
cons_no_turn_x = np.zeros(31)  
cons_right_turn_x = np.zeros(32)  
cons_left_turn_x = np.zeros(33)  
cons_100_x = np.zeros(5)
cons_bill_x = np.zeros(6)

temp_stop_data = np.loadtxt(STOP_FILE_NAME)
temp_walk_data = np.loadtxt(WALK_FILE_NAME)
index = 0
temp = []
for i in temp_stop_data:
    temp.append(abs(i))
    index = index + 1
    if(index == 500):
        stop_data.append(temp)
        temp = []
        index = 0
index = 0        
temp = []        
for i in temp_walk_data:      
    temp.append(abs(i))            
    index = index + 1         
    if(index == 500):         
        walk_data.append(temp)
        temp = []
        index = 0
stop_data = signal.lfilter(b,a,stop_data)
walk_data = signal.lfilter(b,a,walk_data)
cons_no_move_x = np.zeros(len(stop_data))
cons_walk_x = np.zeros(len(walk_data))

'''for i in range(32):
    stop_data.append(np.loadtxt(STOP_FILE_NAME+str(i+1)+".txt"))
for i in range(35):
    walk_data.append(np.loadtxt(WALK_FILE_NAME+str(i+1)+".txt"))
for i in range(25):
    run_data.append(np.loadtxt(RUN_FILE_NAME+str(i+1)+".txt"))
for i in range(31):
    no_turn_data.append(np.loadtxt(NO_TURN_FILE_NAME+str(i+1)+".txt"))
for i in range(32):
    turn_right_data.append(np.loadtxt(TURN_RIGHT_FILE_NAME+str(i+1)+".txt"))
for i in range(33):
    turn_left_data.append(np.loadtxt(TURN_LEFT_FILE_NAME+str(i+1)+".txt"))

for i in range(5):
    one_data.append(np.loadtxt(ONE_NAME+str(i+1)+".txt"))
for i in range(6):
    bill_data.append(np.loadtxt(BILL_NAME+str(i+1)+".txt"))
'''
#std
plt.figure(num=1)

for unit in stop_data:
    stop_std.append(abs(np.std(unit)))    
for unit in walk_data:
    walk_std.append(abs(np.std(unit)))
'''
for unit in run_data:
    run_std.append(abs(np.std(unit)))
for unit in no_turn_data:
    no_turn_std.append(np.std(unit))
for unit in turn_right_data:
    turn_right_std.append(np.std(unit))
for unit in turn_left_data:           
    turn_left_std.append(np.std(unit))
for unit in one_data:
    one_std.append(np.std(unit))
for unit in bill_data:
    bill_std.append(np.std(unit))
'''

plt.scatter(cons_no_move_x,stop_std,label = "stop")
plt.scatter(cons_walk_x,walk_std,label = "walk")
#plt.scatter(cons_run_x,run_std,label = "run")
#plt.scatter(cons_no_turn_x,no_turn_std,label = "no turn")
#plt.scatter(cons_right_turn_x,turn_right_std,label = "turn_right")
#plt.scatter(cons_left_turn_x,turn_left_std,label = "turn_left")
#plt.scatter(cons_100_x,one_std,label = "100")
#plt.scatter(cons_bill_x,bill_std,label = "bill")
plt.legend(loc= "upper right")
plt.show()

#median
plt.figure(num=2)
for unit in stop_data:
    stop_median.append(abs(np.median(unit)))
for unit in walk_data:
    walk_median.append(abs(np.median(unit)))
'''
for unit in run_data:
    run_median.append(abs(np.median(unit)))
for unit in no_turn_data:
    no_turn_median.append(np.median(unit))
for unit in turn_right_data:           
    turn_right_median.append(np.median(unit))
for unit in turn_left_data:           
    turn_left_median.append(np.median(unit))
for unit in one_data:
    one_median.append(np.median(unit))
for unit in bill_data:
    bill_median.append(np.median(unit))
'''

plt.scatter(cons_no_move_x,stop_median,label = "stop")
plt.scatter(cons_walk_x,walk_median,label = "walk")
#plt.scatter(cons_run_x,run_median,label = "run")
#plt.scatter(cons_no_turn_x,no_turn_median,label="no turn")
#plt.scatter(cons_right_turn_x,turn_right_median,label = "turn right")
#plt.scatter(cons_left_turn_x,turn_left_median,label = "turn left")
#plt.scatter(cons_100_x,one_median,label = "100")
#plt.scatter(cons_bill_x,bill_median,label = "bill")
plt.legend(loc= "upper right")        
plt.show() 

#average
plt.figure(num=3)

for unit in stop_data:           
    stop_average.append(abs(np.mean(unit)))
for unit in walk_data:           
    walk_average.append(abs(np.mean(unit)))
'''
for unit in run_data:            
    run_average.append(abs(np.mean(unit)))
for unit in no_turn_data:
    no_turn_average.append(np.average(unit))
for unit in turn_right_data:           
    turn_right_average.append(np.average(unit))
for unit in turn_left_data:           
    turn_left_average.append(np.average(unit))
for unit in one_data:
    one_average.append(np.average(unit))
for unit in bill_data:
    bill_average.append(np.average(unit))
'''

plt.scatter(cons_no_move_x,stop_average,label = "stop")
plt.scatter(cons_walk_x,walk_average,label = "walk")
#plt.scatter(cons_run_x,run_average,label = "run")
#plt.scatter(cons_no_turn_x,no_turn_average,label="no turn")
#plt.scatter(cons_right_turn_x,turn_right_average,label = "turn right")
#plt.scatter(cons_left_turn_x,turn_left_average,label = "turn left")
#plt.scatter(cons_100_x,one_average,label = "100")
#plt.scatter(cons_bill_x,bill_average,label = "bill")
plt.legend(loc= "upper right")        
plt.show()

