#!/usr/bin/python
import smbus
import math
import time
from scipy import signal
 
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

# 1:320
bus = smbus.SMBus(1) # bus = smbus.SMBus(0) fuer Revision 1
address = 0x68       # via i2cdetect
bus.write_byte_data(address, power_mgmt_1, 0)  #initiate mpu6500
bus.write_byte_data(address, 0x37, 0x02) #initiate bypass

mag_address = 0x0c
bus.write_byte_data(mag_address, 0x0A, 0b0110) #initiate AKB8963

record_f = open('record.txt','w')  #the data of bes
time_f = open('time.txt','w') #the data of bes time
lfilter_record_f = open('lfilter_record.txt', 'w') #the data of mag

order = 3
Wn = 0.05
b,a = signal.butter(order,Wn,'low')

i = 0

time_sum = 0
start = 0
end = 0

while i <= 10000:

    beschleunigung_xout = read_word_2c(0x3b, address)
    beschleunigung_yout = read_word_2c(0x3d, address)
    beschleunigung_zout = read_word_2c(0x3f, address)

    beschleunigung_yout_skaliert = beschleunigung_yout / 16384.0 * 9.8

    if i == 0:
        bes_arr = [beschleunigung_yout_skaliert]
        bes_c = str(beschleunigung_yout_skaliert)
        record_f.write(bes_c)
        record_f.write(" ")
        start = time.time()
    else:
        bes_arr.append(beschleunigung_yout_skaliert)
        bes_c = str(beschleunigung_yout_skaliert)
        record_f.write(bes_c)
        record_f.write(" ")

    end = time.time()
    time_sum = time_sum + (end - start) 
    t = str(time_sum)
    time_f.write(t)
    time_f.write(" ")
    start = end
    i = i + 1

y = signal.medfilt(bes_arr,99)
#z = signal.lfilter(b,a,y)

for i in y:
    c = str(i)
    lfilter_record_f.write(c)
    lfilter_record_f.write(" ")
