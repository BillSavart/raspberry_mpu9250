from scipy import signal

stop_f = open('stop.txt', 'r')
walk_f = open('walk.txt', 'r')

stop_filt_f = open('stop_filt.txt', 'w')
walk_filt_f = open('walk_filt.txt', 'w')

stop_arr = []
walk_arr = []

order = 3
wn = 0.003
b,a = signal.butter(order, wn, 'low')

lines = stop_f.readlines()

for line in lines:
	stop_arr.append(float(line.strip('\n')))
	
lines2 = walk_f.readlines()

for line in lines2:
	walk_arr.append(float(line.strip('\n')))

y = signal.lfilter(b,a, stop_arr)
y1 = signal.lfilter(b,a, walk_arr)

for i in y:
	c = str(i)
	stop_filt_f.write(c)
	stop_filt_f.write('\n')

for i in y1:
	c = str(i)
	walk_filt_f.write(c)
	walk_filt_f.write('\n')
