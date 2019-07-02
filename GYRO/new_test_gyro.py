import smbus
import time
import math

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
#main
bus = smbus.SMBus(1) 
address = 0x68       # via i2cdetect
bus.write_byte_data(address, power_mgmt_1, 0)

count = 1

while count <= 100:
	print('count: ', count)
	end = 0
	start = 0
	turn_file = open('./turning_data/left_turn' + str(count) + '.txt', 'w')

	if start == 0:
		start = time.time()

	while end - start < 0.5:
		gyro_xout = read_gyro() #read information from gyro
		x_out = (gyro_xout * 250) / 131	

		c = str(x_out)
		turn_file.write(c)
		turn_file.write('\n')
		end = time.time()
	count = count + 1
