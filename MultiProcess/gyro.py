import smbus
import time
import math
import socket
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

def get_bes(mutex, distance, dis_flag):
	global real_bes
	global stop_key
	bes_arr = []
	while True:
		#print(mp.current_process())
		bes_arr.append(read_bes_y())
		if len(bes_arr) >= 500:
			real_bes = np.std(bes_arr)
			if real_bes <= 0.5 and real_bes > 0:
				pass
			elif real_bes > 0.5 and real_bes < 2:
				mutex.acquire()
				distance.value = distance.value + 0.1
				mutex.release()
			else:
				mutex.acquire()
				distance.value = distance.value + 0.2
				mutex.release()
			bes_arr = []
			dis_flag.value = 1
		if stop_key == True:
			break

def check_turning(mutex, turn, turn_flag):
	global real_gyro
	global stop_key
	gyro_arr = []
	while True:
		#print(mp.current_process())
		gyro_arr.append((read_gyro() * 250) / 131)
		if len(gyro_arr) >= 500:
			real_gyro = np.median(gyro_arr)
			if real_gyro <= 2000 and real_gyro >= -2000:
				mutex.acquire()
				turn.value = 0
				mutex.release()
			elif real_gyro > 2000:
				mutex.acquire()
				turn.value = turn.value + 1
				mutex.release()
			elif real_gyro < -2000:
				mutex.acquire()
				turn.value = turn.value - 1
				mutex.release()
			else:
				pass
			turn_flag.value = 1
			gyro_arr = []
		if stop_key == True:
			break

#main
bus = smbus.SMBus(1) 
address = 0x68       # via i2cdetect
bus.write_byte_data(address, power_mgmt_1, 0)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST,PORT))

mutex = mp.Lock()

distance = mp.Value("d", 0)
turn = mp.Value("i", 0)

turn_flag = mp.Value("i", 0)
dis_flag = mp.Value("i", 0)

p = mp.Process(target=get_bes, args=(mutex, distance, dis_flag))
p1 = mp.Process(target=check_turning, args=(mutex, turn, turn_flag))
p.start()
p1.start()

try:
	while True:
		#print(mp.current_process())
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
					#print("HELP")
					help_flag = True

				elif time.time() - start_warning_time >= 10:
					s.send("HELP2")
					data = s.recv(1024)
					print(data)
					#print("HELP2")
		else:
			start_warning_time = 0
			help_flag = False

		#send bes
		mutex.acquire()
		if help_flag == False and dis_flag.value == 1:
			#print(distance.value)
			temp_dis = str(distance.value)
			s.send(temp_dis)
			data = s.recv(1024)
			print(data)
			distance.value = 0
			dis_flag.value = 0
		mutex.release()

		#send turning
		if help_flag == False and turn_flag.value == 1:
			mutex.acquire()
			turn.value = turn.value % 4
			if turn.value == 0:
				s.send("No Turn")
				data = s.recv(1024)
				print(data)
				#print("No Turn")
				#pass
			elif turn.value == 1:
				s.send("Right")
				data = s.recv(1024)
				print(data)
				#print("Right")
			elif turn.value == 2:
				s.send("Right")
				data = s.recv(1024)
				print(data)
				s.send("Right")
				data = s.recv(1024)
				print(data)
				#print("RightRight")
			else:
				s.send("Left")
				data = s.recv(1024)
				print(data)
				#print("Left")
			turn.value = 0
			turn_flag.value = 0
			mutex.release()
finally:
	stop_key = True
	s.close()
	print("close")
