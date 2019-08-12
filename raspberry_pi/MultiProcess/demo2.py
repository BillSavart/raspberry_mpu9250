#Fix Problem
#	 1. eliminate walk right after turn
#	 2. fix the problem cannot turn immediately after a turn
#	 3. change loop delay to time.sleep
#	 4. cancel if turning_flag == false in the walking if
#	 5. ensure eliminate the floating data after back from help
#	 6. delete the floating data for 5 sec before help data appear

# More To Fix

import socket
import smbus
import time
import math
import numpy as np
import multiprocessing as mp

HOST = '192.168.68.100'
PORT = 8888

# Register
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

# Variable
start = 0  #for time interval
start_warning_time = 0
help_flag = False
real_bes = 0
real_gyro = 0
stop_key = False
turning_flag = False

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

def read_bes_x():
	bes_x = read_word_2c(0x3b)
	bes_y = read_word_2c(0x3d)
	bes_z = read_word_2c(0x3f)

	bes_x_ska = bes_x / 16384.0 * 9.8
	return bes_x_ska

def read_bes_z():
	bes_x = read_word_2c(0x3b)
	bes_y = read_word_2c(0x3d)
	bes_z = read_word_2c(0x3f)

	bes_z_ska = bes_z / 16384.0 * 9.8
	return bes_z_ska

def get_bes(mutex, distance, dis_flag):
	global real_bes
	global stop_key
	global help_flag
	bes_arr = []

	while True:
		temp_data = read_bes_z()
		bes_arr.append(temp_data)
		if len(bes_arr) >= 100:
			real_bes = np.std(bes_arr)
			print('real_bes: ', real_bes)
			mutex.acquire()
			if (real_bes <= 0.3 and real_bes > 0):
				distance.value += 0.0
			else:
				distance.value = distance.value + 1.3
			mutex.release()
			bes_arr = []
			#print(distance.value)
		if stop_key == True:
			break

def check_turning(mutex, turn, turn_flag):
	global real_gyro
	global stop_key
	while True:
		turn.value = read_gyro()
		mutex.acquire()
		if turn.value >= -12000 and turn.value <= 12000:
			turn_flag.value = 0 #no turn
		elif turn.value < 12000:
			turn_flag.value = 1 #left
		else:
			turn_flag.value = 2 #right
		mutex.release()
		
		if stop_key == True:
			break

#main
bus = smbus.SMBus(1) 
address = 0x68       # via i2cdetect
bus.write_byte_data(address, power_mgmt_1, 0)

mutex = mp.Lock()

distance = mp.Value("d", 0)
turn = mp.Value("d", 0)

turn_flag = mp.Value("i", 0)
dis_flag = mp.Value("i", 0)

p = mp.Process(target=get_bes, args=(mutex, distance, dis_flag))
p1 = mp.Process(target=check_turning, args=(mutex, turn, turn_flag))
p.start()
p1.start()

turn_wait_time = 0
help_wait_time = 0

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST,PORT))

s.send((("Stark").encode()).ljust(16))
print("Stark")
time.sleep(1)
s.send((("0.0").encode()).ljust(16))
print("0.0")
time.sleep(3)
s.send((("0.0").encode()).ljust(16))
print("0.0")

try:
	delay_times = 0
	while True:
		#check if falling
		bes_xout = read_bes_x()
		#print("help: ", bes_xout)
		if bes_xout > -4.0:
			help_wait_time = time.time()
			if start_warning_time == 0:
				start_warning_time = time.time()
				print("START HELP")
				time.sleep(1)
			else:
				if time.time() - start_warning_time >= 5 and time.time() - start_warning_time < 10:
					s.send((("HELP").encode()).ljust(16))
					print("HELP")
					help_flag = True
				elif time.time() - start_warning_time >= 10:
					s.send((("HELP2").encode()).ljust(16))
					print("HELP2")
		else:
			start_warning_time = 0
			help_flag = False

		#send turning
		if help_flag == False:
			if turn_flag.value == 0:
				#print("No Turn")
				turning_flag = False
				
			elif turn_flag.value == 1 and time.time() - help_wait_time > 2:
				turning_flag = True
				s.send((("Left").encode()).ljust(16))
				print("Left")
				time.sleep(1)
				turn_wait_time = time.time()
				help_wait_time = 0
			elif time.time() - help_wait_time > 2:
				turning_flag = True
				s.send((("Right").encode()).ljust(16))
				print("Right")
				time.sleep(1)
				turn_wait_time = time.time()
				help_wait_time = 0
			else:
				pass
			turning_flag = False
			turn.value = 0
			turn_flag.value = 0
		else:
			turn.value = 0
			turn_flag.value = 0

		if help_flag == False and time.time() - turn_wait_time > 2 and time.time() - help_wait_time > 2 and distance.value != 0:
			temp_dis = str(distance.value)
			s.send(((temp_dis).encode()).ljust(16))
			print(temp_dis)
			distance.value = 0
			time.sleep(0.15)
			turn_wait_time = 0
			help_wait_time = 0
		else:
			distance.value = 0
finally:
	stop_key = True
	print("close")
