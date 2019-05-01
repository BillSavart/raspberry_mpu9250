import smbus
import math
import time

# Register
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c
 
def read_byte(reg, addr):
    return bus.read_byte_data(addr, reg)
 
def read_word(reg, addr):
    h = bus.read_byte_data(addr, reg)
    l = bus.read_byte_data(addr, reg+1)
    value = (h << 8) + l
    return value
 
def read_word_2c(reg, addr):
    val = read_word(reg, addr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

# 1:320 for map information
bus = smbus.SMBus(1) # bus = smbus.SMBus(0) fuer Revision 1
address = 0x68       # via i2cdetect
bus.write_byte_data(address, power_mgmt_1, 0)  #initiate mpu6500

start_warning_time = 0
while True:	
	bes_x = read_word_2c(0x3b, address)
	bes_y = read_word_2c(0x3d, address)
	bes_z = read_word_2c(0x3f, address)

	bes_x_ska = bes_x / 16384.0 * 9.8
	print "bes_x_ska: " , bes_x_ska
	print

	if bes_x_ska > -9:
		if start_warning_time == 0:
			start_warning_time = time.time()
		else:
			if time.time() - start_warning_time > 5:
				print "HELPPPPP!!!!!!!!!!!!!!!!!!" 
	else:
		start_warning_time = 0

