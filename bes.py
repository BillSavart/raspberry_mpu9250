#!/usr/bin/python
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

bus = smbus.SMBus(1) # bus = smbus.SMBus(0) fuer Revision 1
address = 0x68       # via i2cdetect
bus.write_byte_data(address, power_mgmt_1, 0)  #initiate mpu6500
bus.write_byte_data(address, 0x37, 0x02) #initiate bypass

mag_address = 0x0c
bus.write_byte_data(mag_address, 0x0A, 0b0110) #initiate AKB8963

record_f = open('record.txt','w')  #the data of bes
time_f = open('time.txt','w') #the data of bes time
mag_record_f = open('mag_record.txt', 'w') #the data of mag
mag_time_f = open('mag_time.txt', 'w') #the data of mag time

t = 0

# Aktivieren, um das Modul ansprechen zu koennen
bus.write_byte_data(address, power_mgmt_1, 0)

speed = 0
start = 0 #bes time
prev = 0 #mag data
now = 0 #mag data
count_mag_time = 0 #mag delay

while True:
    beschleunigung_xout = read_word_2c(0x3b, address)
    beschleunigung_yout = read_word_2c(0x3d, address)
    beschleunigung_zout = read_word_2c(0x3f, address)

    beschleunigung_yout_skaliert = beschleunigung_yout / 16384.0 * 9.8

    mag_xout = read_word_2c(0x04, mag_address)
    mag_yout = read_word_2c(0x06, mag_address)
    mag_zout = read_word_2c(0x08, mag_address)

    if start == 0:
        start = time.time()
        prev = mag_yout

    end = time.time()  
    time_interval = end - start

    count_mag_time = count_mag_time + 1
    if count_mag_time == 700:
        count_mag_time = 0
        now = mag_yout
        #count if stop
        if prev - now > -5 and prev - now < 5:
           pass  #   print "no move"
        else:
            print "move"
            #the bes value is valid
        prev = now

    if beschleunigung_yout_skaliert < 1 and beschleunigung_yout_skaliert > -1:
        pass
    else:
        speed = speed + (time_interval * beschleunigung_yout_skaliert)
        print "beschleunigung_yout: ", beschleunigung_yout_skaliert
        print "speed: ", speed

    s = str(beschleunigung_yout_skaliert)
    #record_f.write(s)
    #record_f.write(' ')
        
    t = t + time_interval
    t1 = str(t)
    #time_f.write(t1)
    #time_f.write(' ')
        
    start = end
    prev = now
