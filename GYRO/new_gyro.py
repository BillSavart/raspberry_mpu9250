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

sum_l = 0  #for turning
sum_r = 0  

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

def turning_recognition(x, sum_L, sum_R):
	if x > -4 and x < 4:
		x = 0

	if x == 0:
		return "Straight"

	elif x > 0:
		sum_L = 0
		sum_R = sum_R + x

		if sum_R > 18000:
			sum_R = 0
			#print "Turn Right"
			return "Right"
		else:
			return "Straight"
	else:
		sum_R = 0
		sum_L = sum_L + x

		if sum_L < -18000:
			sum_L = 0
			#print "Turn Left"
			return "Left"
		else:
			return "Straight"

def falling(yout):
	print "yout" , yout

def skt(message, s):
	try:
		#cmd = raw_input("Please input msg:")
		s.send(message)
		data = s.recv(1024)
		print(data)
	finally:
		pass
		#s.close()
		#print('close')

#main
bus = smbus.SMBus(1) 
address = 0x68       # via i2cdetect
bus.write_byte_data(address, power_mgmt_1, 0)

sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sk.connect((HOST, PORT))

#file
data_f = open('data.txt', 'w')
time_f = open('time.txt', 'w')
time_sum = 0
file_start = 0
file_end = 0

while True:
	if start == 0:
		start = time.time()

	end = time.time()
	time_interval = end - start

	gyro_xout = read_gyro() #read information from gyro
	x_out = (gyro_xout * 250 * time_interval) / 131
	#data_f.write(x_out)
	#data_f.write(" ")
	#time_sum = time_sum + time_interval

	#check if turning or not
	turn = turning_recognition(x_out, sum_l, sum_r)

	#socket
	skt(turn, sk)


	#falling(x_out)

	start = end
	time.sleep(1)
