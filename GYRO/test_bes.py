import smbus
import time
import math
from scipy import signal

# Register
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

# Variable
start = 0  #for time interval
start_warning_time = 0
help_flag = False

def read_byte(reg):
	return bus.read_byte_data(address, reg)

def read_word(reg):
	h = bus.read_byte_data(address, reg)
	l = bus.read_byte_data(address, reg+1)
	value = (h << 8) + l
	return value

def read_word_2c(reg):
	val = read_word(reg)
	if (val >= 0x8000):
		return -((65535 - val) + 1)
	else:
		return val

def read_gyro():
	xout = read_word_2c(0x43)
	yout = read_word_2c(0x45)
	zout = read_word_2c(0x47)
	return xout

def turning_recognition(x,T):
	if x >= -10000 and x <= 10000:
		return "No Turn"
	elif x > 10000:
		return "Right"
	elif x < -10000:
		return "Left"

def read_bes_x():
	bes_x = read_word_2c(0x3b)
	bes_y = read_word_2c(0x3d)
	bes_z = read_word_2c(0x3f)

	bes_x_ska = bes_x / 16384.0 * 9.8
	return bes_x_ska

def read_bes_y():
	bes_x = read_word_2c(0x3b)
	bes_y = read_word_2c(0x3d)
	bes_z = read_word_2c(0x3f)

	bes_y_ska = bes_y / 16384.0 * 9.8
	return bes_y_ska

#main
bus = smbus.SMBus(1) 
address = 0x68       # via i2cdetect
bus.write_byte_data(address, power_mgmt_1, 0)

#FILTER
order = 3
Wn = 0.003
b,a = signal.butter(order, Wn, 'low')

count = 5

i=1
while i <= count:
####### FILE################
	record_f = open('./data/test_walk'+str(i)+'.txt', 'w')
	time_f = open('./data/test_walk_time'+str(i)+'.txt', 'w')
	count_file = 0
	start = 0
	real_start = 0
	end = 0
	while end - real_start <= 0.5:
		if start == 0:
			start = time.time()
			real_start = time.time()

		end = time.time()
		time_interval = end - start
		
		bes_yout = read_bes_y()
		c = str(bes_yout)
		record_f.write(c)
		record_f.write("\n")
		time_string = str(time_interval)
		time_f.write(time_string)
		time_f.write("\n")
		start = end
	i = i + 1	
