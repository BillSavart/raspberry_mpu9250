import smbus
import time
import math
import socket
import numpy as np
import threading
from scipy import signal

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
	while True:
		global real_bes
		mutex.acquire()
		real_bes = read_bes_y()
		print('real_bes:' , real_bes)
		mutex.release()

def check_turning():
	while True:
		global real_gyro
		mutex.acquire()
		real_gyro = ((read_gyro() * 250) / 131)
		print('real_gyro:' , real_gyro)
		mutex.release()

mutex = threading.Lock()

#main
bus = smbus.SMBus(1) 
address = 0x68       # via i2cdetect
bus.write_byte_data(address, power_mgmt_1, 0)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST,PORT))

#FILTER
order = 3
Wn = 0.003
b,a = signal.butter(order, Wn, 'low')

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
		mutex.acquire()
		s.send("b" + str(real_bes))
		data = s.recv(1024)
		print(data)
		mutex.release()

		#send turning
		mutex.acquire()
		s.send("g" + str(real_gyro))
		data = s.recv(1024)
		print(data)
		mutex.release()
finally:
	t.join()
	t1.join()
	s.close()
	print "close"
