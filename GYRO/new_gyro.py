import smbus
import time
import math
import socket

HOST = '192.168.68.97'
PORT = 7777

# Register
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

# Variable
start = 0  #for time interval

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

def falling(yout):
	print "yout" , yout

#main
bus = smbus.SMBus(1) 
address = 0x68       # via i2cdetect
bus.write_byte_data(address, power_mgmt_1, 0)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST,PORT))

try:
	while True:
		if start == 0:
			start = time.time()

		end = time.time()
		time_interval = end - start

		gyro_xout = read_gyro() #read information from gyro
		x_out = (gyro_xout * 250 * time_interval) / 131

		#check if turning or not
		turn = turning_recognition(x_out,time_interval)

		#socket
		s.send(turn)
		data = s.recv(1024)
		print(data)

		#falling(x_out)

		start = end
finally:
	s.close()
	print "close"
