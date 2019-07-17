import smbus
import time
import math
import socket
import numpy as np
from scipy import signal

# Register
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

def read_byte(reg):
	return bus.read_byte_data(address, reg)

def read_word(reg,address):
	h = bus.read_byte_data(address, reg)
	l = bus.read_byte_data(address, reg+1)
	value = (h << 8) + l
	return value

def read_word_2c(reg,addr):
	val = read_word(reg,addr)
	if (val >= 0x8000):
		return -((65535 - val) + 1)
	else:
		return val

def read_gyro_x(addr):
	xout = read_word_2c(0x43,addr)
	yout = read_word_2c(0x45,addr)
	zout = read_word_2c(0x47,addr)
	return xout

def read_gyro_y(addr):
    xout = read_word_2c(0x43,addr)
    yout = read_word_2c(0x45,addr)
    zout = read_word_2c(0x47,addr)
    return yout

def read_gyro_z(addr):
    xout = read_word_2c(0x43,addr)
    yout = read_word_2c(0x45,addr)
    zout = read_word_2c(0x47,addr)
    return zout

def read_bes_x(addr):
	bes_x = read_word_2c(0x3b,addr)
	bes_y = read_word_2c(0x3d,addr)
	bes_z = read_word_2c(0x3f,addr)

	bes_x_ska = bes_x / 16384.0 * 9.8
	return bes_x_ska

def read_bes_y(addr):
	bes_x = read_word_2c(0x3b,addr)
	bes_y = read_word_2c(0x3d,addr)
	bes_z = read_word_2c(0x3f,addr)

	bes_y_ska = bes_y / 16384.0 * 9.8
	return bes_y_ska

def read_bes_z(addr):
	bes_x = read_word_2c(0x3b,addr)
	bes_y = read_word_2c(0x3d,addr)
	bes_z = read_word_2c(0x3f,addr)

	bes_z_ska = bes_z / 16384.0 * 9.8
	return bes_z_ska

def read_mag_x(addr):
	mag_x = read_word_2c(0x04,addr)
	mag_y = read_word_2c(0x06,addr)
	mag_z = read_word_2c(0x08,addr)

	mag_x_out = mag_x
	return mag_x_out

def read_mag_y(addr):
    mag_x = read_word_2c(0x04,addr)
    mag_y = read_word_2c(0x06,addr)
    mag_z = read_word_2c(0x08,addr)

    mag_y_out = mag_y
    return mag_y_out

def read_mag_z(addr):
    mag_x = read_word_2c(0x04,addr)
    mag_y = read_word_2c(0x06,addr)
    mag_z = read_word_2c(0x08,addr)

    mag_z_out = mag_z
    return mag_z_out


bus = smbus.SMBus(1) 
address = 0x68       # via i2cdetect
bus.write_byte_data(address, power_mgmt_1, 0)
bus.write_byte_data(address, 0x37,0x02)
mag_address = 0x0c
bus.write_byte_data(mag_address,0x0A, 0b0110)
start_t = 0
end_t = 0

count = 0

bes_arr_x = []
bes_arr_y = []
bes_arr_z = []
gyro_arr_x = []
gyro_arr_y = []
gyro_arr_z = []

while count < 50:
	bes_arr_x.append(read_bes_x(address))
	bes_arr_y.append(read_bes_y(address))
	bes_arr_z.append(read_bes_z(address))
	gyro_arr_x.append(read_gyro_x(address))
	gyro_arr_y.append(read_gyro_y(address))
	gyro_arr_z.append(read_gyro_z(address))
	count = count + 1

bes_bias_x = np.average(bes_arr_x)
bes_bias_y = np.average(bes_arr_y)
bes_bias_z = np.average(bes_arr_z) + 0.981
gyro_bias_x = np.average(gyro_arr_x)
gyro_bias_y = np.average(gyro_arr_y)
gyro_bias_z = np.average(gyro_arr_z)

print(bes_bias_x)
print(bes_bias_y)
print(bes_bias_z)
print(gyro_bias_x)
print(gyro_bias_y)
print(gyro_bias_z)

while True:
	gyro_x = read_gyro_x(address)
	gyro_y = read_gyro_y(address)
	gyro_z = read_gyro_z(address)
	bes_x = read_bes_x(address)
	bes_y = read_bes_y(address)
	bes_z = read_bes_z(address)
	mag_x = read_mag_x(mag_address)
	mag_y = read_mag_y(mag_address)
	mag_z = read_mag_z(mag_address)

	q0 = 1
	q1 = 0
	q2 = 0
	q3 = 0
	
	beta = 0.005

	qDot1 = 0.5 * (-q1 * gyro_x - q2 * gyro_y - q3 * gyro_z)
	qDot2 = 0.5 * (q0 * gyro_x + q2 * gyro_z - q3 * gyro_y)
	qDot3 = 0.5 * (q0 * gyro_y - q1 * gyro_z + q3 * gyro_x)
	qDot4 = 0.5 * (q0 * gyro_z + q1 * gyro_y - q2 * gyro_x)

	if(not((bes_x == 0) and (bes_y == 0) and (bes_z == 0))):
		recipNorm = 1.0 / (math.sqrt(bes_x * bes_x + bes_y * bes_y + bes_z * bes_z))
		bes_x = bes_x * recipNorm
		bes_y = bes_y * recipNorm
		bes_z = bes_z * recipNorm

		sampleFreq = 100

		_2q0 = 2.0 * q0
		_2q1 = 2.0 * q1
		_2q2 = 2.0 * q2
		_2q3 = 2.0 * q3

		_4q0 = 4.0 * q0
		_4q1 = 4.0 * q1
		_4q2 = 4.0 * q2
	
		_8q1 = 8.0 * q1
		_8q2 = 8.0 * q2
			
		q0q0 = q0 * q0
		q1q1 = q1 * q1
		q2q2 = q2 * q2
		q3q3 = q3 * q3

		s0 = _4q0 * q2q2 + _2q2 * bes_x + _4q0 * q1q1 - _2q1 * bes_y
		s1 = _4q1 * q3q3 - _2q3 * bes_x + 4.0 * q0q0 * q1 - _2q0 * bes_y - _4q1 + _8q1 * q1q1 + _8q1 * q2q2 + _4q1 * bes_z
		s2 = 4.0 * q0q0 * q2 + _2q0 * bes_x + _4q2 * q3q3 - _2q3 * bes_y - _4q2 + _8q2 * q1q1 + _8q2 * q2q2 + _4q2 * bes_z
		s3 = 4.0 * q1q1 * q3 - _2q1 * bes_x + 4.0 * q2q2 * q3 - _2q2 * bes_y

		recipNorm = 1.0 / (math.sqrt(s0*s0+s1*s1+s2*s2+s3*s3))
		s0 = s0 * recipNorm
		s1 = s1 * recipNorm
		s2 = s2 * recipNorm
		s3 = s3 * recipNorm

		qDot1 = qDot1 - beta * s0
		qDot2 = qDot2 - beta * s1
		qDot3 = qDot3 - beta * s2
		qDot4 = qDot4 - beta * s3

	q0 = q0 + qDot1 * (1.0 / sampleFreq)
	q1 = q1 + qDot2 * (1.0 / sampleFreq)
	q2 = q2 + qDot3 * (1.0 / sampleFreq)
	q3 = q3 + qDot4 * (1.0 / sampleFreq)

	recipNorm = 1.0 / (math.sqrt(q0*q0+q1*q1+q2*q2+q3*q3))
	q0 = q0 * recipNorm
	q1 = q1 * recipNorm
	q2 = q2 * recipNorm
	q3 = q3 * recipNorm

	roll = (math.atan2(q0*q1 + q2*q3 , 0.5 - q1*q1 - q2*q2)) * (180.0 / math.pi)
	pitch = (math.asin(-2.0 * (q1*q3 - q0 * q2))) * (180.0 / math.pi)
	yaw = (math.atan2(q1*q2 + q0*q3 , 0.5 - q2*q2 - q3*q3)) *(180.0 / math.pi)

#	print(roll)
#	print(pitch)
	#print(yaw)
	#print	