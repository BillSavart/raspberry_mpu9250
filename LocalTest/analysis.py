import numpy as np
import matplotlib.pyplot as plt

DATA_NUM = 100
STOP_FILE_NAME = "../GYRO/data/test_stop"
WALK_FILE_NAME = "../GYRO/data/test_walk"
RUN_FILE_NAME = "../GYRO/data/test_run"
NO_TURN_FILE_NAME = "../GYRO/turning_data/no_turn"
TURN_RIGHT_FILE_NAME = "../GYRO/turning_data/right_turn"
TURN_LEFT_FILE_NAME = "../GYRO/turning_data/left_turn"

stop_data = []
walk_data = []
run_data = []
no_turn_data = []
turn_right_data = []
turn_left_data = []

stop_std = []
walk_std = []
run_std = []
no_turn_std = []
turn_right_std = []
turn_left_std = []

stop_median = []
walk_median = []
run_median = []
no_turn_median = []
turn_right_median = []
turn_left_median = []

stop_average = []
walk_average = []
run_average = []
no_turn_average = []
turn_right_average = []
turn_left_average = []

for i in range(DATA_NUM):
    stop_data.append(np.loadtxt(STOP_FILE_NAME+str(i+1)+".txt"))
for i in range(DATA_NUM):
    walk_data.append(np.loadtxt(WALK_FILE_NAME+str(i+1)+".txt"))
for i in range(DATA_NUM):
    run_data.append(np.loadtxt(RUN_FILE_NAME+str(i+1)+".txt"))
for i in range(DATA_NUM):
    no_turn_data.append(np.loadtxt(NO_TURN_FILE_NAME+str(i+1)+".txt"))
for i in range(DATA_NUM):
    turn_right_data.append(np.loadtxt(TURN_RIGHT_FILE_NAME+str(i+1)+".txt"))
for i in range(DATA_NUM):
    turn_left_data.append(np.loadtxt(TURN_LEFT_FILE_NAME+str(i+1)+".txt"))

#std
plt.figure(num=1)
constant_x = np.zeros(DATA_NUM)
for unit in stop_data:
    stop_std.append(abs(np.std(unit)))    
for unit in walk_data:
    walk_std.append(abs(np.std(unit)))
for unit in run_data:
    run_std.append(abs(np.std(unit)))
for unit in no_turn_data:
    no_turn_std.append(np.std(unit))
for unit in turn_right_data:
    turn_right_std.append(np.std(unit))
for unit in turn_left_data:           
    turn_left_std.append(np.std(unit))

#plt.scatter(constant_x,stop_std,label = "stop")
#plt.scatter(constant_x,walk_std,label = "walk")
#plt.scatter(constant_x,run_std,label = "run")
plt.scatter(constant_x,no_turn_std,label = "no turn")
plt.scatter(constant_x,turn_right_std,label = "turn_right")
plt.scatter(constant_x,turn_left_std,label = "turn_left")
plt.legend(loc= "upper right")
plt.show()

#median
plt.figure(num=2)
for unit in stop_data:
    stop_median.append(abs(np.median(unit)))
for unit in walk_data:
    walk_median.append(abs(np.median(unit)))
for unit in run_data:
    run_median.append(abs(np.median(unit)))
for unit in no_turn_data:
    no_turn_median.append(np.median(unit))
for unit in turn_right_data:           
    turn_right_median.append(np.median(unit))
for unit in turn_left_data:           
    turn_left_median.append(np.median(unit))

#plt.scatter(constant_x,stop_median,label = "stop")
#plt.scatter(constant_x,walk_median,label = "walk")
#plt.scatter(constant_x,run_median,label = "run")
plt.scatter(constant_x,no_turn_median,label="no turn")
plt.scatter(constant_x,turn_right_median,label = "turn right")
plt.scatter(constant_x,turn_left_median,label = "turn left")
plt.legend(loc= "upper right")        
plt.show() 

#average
plt.figure(num=3)
for unit in stop_data:           
    stop_average.append(abs(np.mean(unit)))
for unit in walk_data:           
    walk_average.append(abs(np.mean(unit)))
for unit in run_data:            
    run_average.append(abs(np.mean(unit)))
for unit in no_turn_data:
    no_turn_average.append(np.average(unit))
for unit in turn_right_data:           
    turn_right_average.append(np.average(unit))
for unit in turn_left_data:           
    turn_left_average.append(np.average(unit))

#plt.scatter(constant_x,stop_average,label = "stop")
#plt.scatter(constant_x,walk_average,label = "walk")
#plt.scatter(constant_x,run_average,label = "run")
plt.scatter(constant_x,no_turn_average,label="no turn")
plt.scatter(constant_x,turn_right_average,label = "turn right")
plt.scatter(constant_x,turn_left_average,label = "turn left")
plt.legend(loc= "upper right")        
plt.show() 
