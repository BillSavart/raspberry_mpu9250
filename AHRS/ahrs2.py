import smbus
import time
import math
import socket
import numpy as np
from scipy import signal
from madgwickahrs import MadgwickAHRS
from quaternion import Quaternion

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

	bes_arr = [bes_x, bes_y , bes_z]
	gyro_arr = [gyro_x, gyro_y, gyro_z]
	mag_arr = [mag_x, mag_y, mag_z]

	q = Quaternion(1,0,0,0)
	m = MadgwickAHRS(1/1000,q,1)
	#print("before: ",m.quaternion.q)
	MadgwickAHRS.update(m,bes_arr, gyro_arr, mag_arr)
	#print("after: ",m.quaternion.q)

	roll = math.atan2(2.0*(m.quaternion.q[2] * m.quaternion.q[3] + m.quaternion.q[0] * m.quaternion.q[1]), m.quaternion.q[0] * m.quaternion.q[0] - m.quaternion.q[1] * m.quaternion.q[1] - m.quaternion.q[2] * m.quaternion.q[2] + m.quaternion.q[3] * m.quaternion.q[3]) * (180.0 / math.pi)
	pitch = math.asin(-2.0 * (m.quaternion.q[1] * m.quaternion.q[3] - m.quaternion.q[0] * m.quaternion.q[2])) * (180.0 / math.pi)
	yaw = math.atan2(2.0*(m.quaternion.q[1]*m.quaternion.q[2] + m.quaternion.q[0] * m.quaternion.q[3]), m.quaternion.q[0] * m.quaternion.q[0] + m.quaternion.q[1] * m.quaternion.q[1] - m.quaternion.q[2] * m.quaternion.q[2] - m.quaternion.q[3] * m.quaternion.q[3]) * (180.0 / math.pi)

	print("qua:", m.quaternion.q[0], m.quaternion.q[1], m.quaternion.q[2], m.quaternion.q[3])
	print("roll:",roll)
	print("pitch:",pitch)
	print("yaw:",yaw)
	print("")
