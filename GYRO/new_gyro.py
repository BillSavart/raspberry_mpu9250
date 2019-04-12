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

sum_r = 0
sum_l = 0

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
	global sum_r
	global sum_l
	print "sumr: ", sum_r
	print "suml: ", sum_l
	print x
	print
	if x >= -10000 and x <= 10000:
		sum_r = 0
		sum_l = 0
		return "No Turn"
	elif x > 10000:
		sum_l = 0
		sum_r += x*T
#		if sum_r >= 15000 or x > 30000:
#			print x
#			sum_r = 0
		return "Right"
	elif x < -10000:
		sum_r = 0
		sum_l += x*T
#		if sum_l <= -15000 or x < -30000:
#			print x
#			sum_l = 0
		return "Left"
#	else:
#		pass 

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

#sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#sk.connect((HOST, PORT))

#file
data_f = open('data.txt', 'w')
time_f = open('time.txt', 'w')
sum_r_f = open('sum_r.txt','w')
sum_l_f = open('sum_l.txt','w')
time_sum = 0

count_time = 0
count_start = 0
count_end = 0
j = 0

while True:
	if start == 0:
		start = time.time()

	end = time.time()
	time_interval = end - start

	gyro_xout = read_gyro() #read information from gyro
	x_out = (gyro_xout * 250 * time_interval) / 131

	x_str = str(x_out)
	data_f.write(x_str)
	data_f.write(" ")
	time_sum = time_sum + time_interval
	t = str(time_sum)
	time_f.write(t)
	time_f.write(" ")

	#check if turning or not
	turn = turning_recognition(x_out,time_interval)
	print turn
	print
	#socket
	#skt(turn, sk)

	#falling(x_out)

	start = end
	#time.sleep(1)
	count_start = time.time()
	while count_time < 800:
		while j < 700:
			j = j + 1
		count_time = count_time + 1
		j = 0

	j = 0
	count_time = 0
	count_end = time.time() - count_start

#	print count_end
