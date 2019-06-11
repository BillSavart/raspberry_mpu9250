import smbus
import time
import math
import socket

HOST = '192.168.68.97'
PORT = 8888

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
		if help_flag == False:
			s.send(turn)
			data = s.recv(1024)
			#print(data)

		#check if falling
		bes_xout = read_bes_x()
		if bes_xout > -9:
			if start_warning_time == 0:
				start_warning_time = time.time()
			else:
				if time.time() - start_warning_time >= 5 and time.time() - start_warning_time < 10:
					s.send("HELP")
					data = s.recv(1024)
					#print(data)
					help_flag = True

				elif time.time() - start_warning_time >= 10:
					s.send("HELP2")
					data = s.recv(1024)
					#print(data)
		else:
			start_warning_time = 0
			help_flag = False
		
		print("x: ", bes_xout)
		print("y: ", read_bes_y())
		print("time: ", time_interval)
		print()
		start = end
finally:
	s.close()
	print "close"
