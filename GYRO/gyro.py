import smbus
import time
import math
import socket
import numpy as np
import threading

HOST = '192.168.68.97'
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
distance = 0
turn = 0
stop_key = False

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

def read_bes_y():
	bes_x = read_word_2c(0x3b)
	bes_y = read_word_2c(0x3d)
	bes_z = read_word_2c(0x3f)

	bes_y_ska = bes_y / 16384.0 * 9.8
	return bes_y_ska

def get_bes():
	global real_bes
	global distance
	global stop_key
	global mutex
	global s
	bes_arr = []

	while True:
		bes_arr.append(read_bes_y())
		if len(bes_arr) >= 100:
			real_bes = np.std(bes_arr)
			if real_bes < 0.2 and real_bes > 0:
				pass
			elif real_bes > 0.2 and real_bes < 1.6:
				mutex.acquire()
				distance = distance + 0.4
				mutex.release()
			else:
				mutex.acquire()
				distance = distance + 1
				mutex.release()
			bes_arr = []
			#print(threading.current_thread())
		if stop_key == True:
			break
	
def check_turning():
	global turn
	global real_gyro
	global stop_key
	global mutex
	global s
	gyro_arr = []
	
	while True:
		gyro_arr.append((read_gyro() * 250) / 131)
		if len(gyro_arr) >= 100:
			real_gyro = np.median(gyro_arr)
			if real_gyro < 2000 and real_gyro > 2000:
				mutex.acquire()
				turn = 0
				mutex.release()
			elif real_gyro > 10000:
				mutex.acquire()
				turn = turn + 1
				mutex.release()
			elif real_gyro < -10000:
				mutex.acquire()
				turn = turn - 1
				mutex.release()
			else:
				pass
			turn = 0
			gyro_arr = []
			#print(threading.current_thread())
		if stop_key == True:
			break
mutex = threading.Lock()

#main
bus = smbus.SMBus(1) 
address = 0x68       # via i2cdetect
bus.write_byte_data(address, power_mgmt_1, 0)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST,PORT))
t = threading.Thread(target = get_bes)
t1 = threading.Thread(target = check_turning)
t.start()
t1.start()

try:
	while True:
		#check if falling
		bes_xout = read_bes_x()
		if bes_xout > -9:
			if start_warning_time == 0:
				start_warning_time = time.time()
			else:
				if time.time() - start_warning_time >= 5 and time.time() - start_warning_time < 10:
					s.send("HELP")
					data = s.recv(1024)
					print(data)
					help_flag = True

				elif time.time() - start_warning_time >= 10:
					s.send("HELP2")
					data = s.recv(1024)
					print(data)
		else:
			start_warning_time = 0
			help_flag = False

		#send bes
		#mutex.acquire()
		if help_flag == False and distance != 0:
			s.send(str(distance))
			data = s.recv(1024)
			print(data)
			distance = 0
		#mutex.release()

		#send turning
		#mutex.acquire()
		if help_flag == False:
			turn = turn % 4
			if turn == 0:
				s.send("No Turn")
				data = s.recv(1024)
				print(data)
			elif turn == 1:
				s.send("Right")
				data = s.recv(1024)
				print(data)
			elif turn == 2:
				s.send("Right")
				data = s.recv(1024)
				print(data)
				s.send("Right")
				data = s.recv(1024)
				print(data)
			else:
				s.send("Left")
				data = s.recv(1024)
				print(data)
			turn = 0
		#mutex.release()
		#print(threading.current_thread())
finally:
	stop_key = True
	s.close()
	print("close")
