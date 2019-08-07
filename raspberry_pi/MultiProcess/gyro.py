import smbus
import time
import math
import socket
import numpy as np
import multiprocessing as mp

HOST = '192.168.208.105'
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
		if len(bes_arr) >= 500:
			real_bes = np.std(bes_arr)
			#print('real_bes: ', real_bes)
			mutex.acquire()
			if (real_bes <= 0.3 and real_bes > 0):
				distance.value = 0.0
			else:
				distance.value = distance.value + 1.2
			mutex.release()
			bes_arr = []

		if stop_key == True:
			break

def check_turning(mutex, turn, turn_flag):
	global real_gyro
	global stop_key
	while True:
		turn.value = read_gyro()
		mutex.acquire()
		if turn.value >= -10000 and turn.value <= 10000:
			turn_flag.value = 0 #no turn
		elif turn.value < -10000:
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

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST,PORT))

s.send(("Mark").ljust(16))
s.send(("0.0").ljust(16))
mutex = mp.Lock()

distance = mp.Value("d", 0)
turn = mp.Value("d", 0)

turn_flag = mp.Value("i", 0)
dis_flag = mp.Value("i", 0)

p = mp.Process(target=get_bes, args=(mutex, distance, dis_flag))
p1 = mp.Process(target=check_turning, args=(mutex, turn, turn_flag))
p.start()
p1.start()

delay = 0

try:
	while True:
		#check if falling
		bes_xout = read_bes_x()
		if bes_xout > -6.0:
			if start_warning_time == 0:
				start_warning_time = time.time()
			else:
				if time.time() - start_warning_time >= 5 and time.time() - start_warning_time < 10:
					s.send(("HELP").ljust(16))
					print("HELP")
					help_flag = True
				elif time.time() - start_warning_time >= 10:
					s.send(("HELP2").ljust(16))
					print("HELP2")
		else:
			start_warning_time = 0
			help_flag = False

		#send turning
		if help_flag == False:
			if turn_flag.value == 0:
				turning_flag = False
				
			elif turn_flag.value == 1:
				turning_flag = True
				s.send(("Left").ljust(16))
				print("Left")
				time.sleep(1)

			else:
				turning_flag = True
				s.send(("Right").ljust(16))
				print("Right")
				time.sleep(1)

			turn.value = 0
			turn_flag.value = 0
		else:
			turn.value = 0
			turn_flag.value = 0

		if turning_flag == False and help_flag == False:
			temp_dis = str(distance.value)
			s.send((temp_dis).ljust(16))
			print(temp_dis)
			distance.value = 0
			while delay < 100000:
				delay += 1
			delay = 0
		else:
			distance.value = 0
		turning_flag = False
finally:
	stop_key = True
	#s.close()
	print("close")
