import numpy as np
import smbus
import time
import math
from scipy import signal

# Register
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

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

def read_bes_z():
	bes_x = read_word_2c(0x3b)
	bes_y = read_word_2c(0x3d)
	bes_z = read_word_2c(0x3f)

	bes_z_ska = bes_z / 16384.0 * 9.8
	return bes_z_ska

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

def read_gyro_x():
	x = read_word_2c(0x43)
	y = read_word_2c(0x45)
	z = read_word_2c(0x47)
	return x

def read_gyro_y():
	x = read_word_2c(0x43)
	y = read_word_2c(0x45)
	z = read_word_2c(0x47)
	return y

def read_gyro_z():
	x = read_word_2c(0x43)
	y = read_word_2c(0x45)
	z = read_word_2c(0x47)
	return z


#main
bus = smbus.SMBus(1) 
address = 0x68       # via i2cdetect
bus.write_byte_data(address, power_mgmt_1, 0)
order = 3
wn = 0.003

b,a = signal.butter(order, wn, 'low')

while True:
#	x = read_bes_x()
#	y = read_bes_y()
#	z = read_bes_z()
	x = read_gyro_x()
	y = read_gyro_y()
	z = read_gyro_z()
	print("g_x: ",x)
	print("g_y: ",y)
	print("g_z: ",z)
#	print("total_bes: ",math.sqrt(x*x+y*y+z*z)-9.8)
	print('\n')
	#time.sleep(1)
