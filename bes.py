#!/usr/bin/python
import smbus
import math
import time
 
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

bus = smbus.SMBus(1) # bus = smbus.SMBus(0) fuer Revision 1
address = 0x68       # via i2cdetect

f = open('record.txt','w')
f1 = open('time.txt','w')

t = 0

# Aktivieren, um das Modul ansprechen zu koennen
bus.write_byte_data(address, power_mgmt_1, 0)

speed = 0
start = 0

while True:
    beschleunigung_xout = read_word_2c(0x3b)
    beschleunigung_yout = read_word_2c(0x3d)
    beschleunigung_zout = read_word_2c(0x3f)
 
    beschleunigung_xout_skaliert = beschleunigung_xout / 16384.0
    beschleunigung_yout_skaliert = beschleunigung_yout / 16384.0 * 9.8
    beschleunigung_zout_skaliert = beschleunigung_zout / 16384.0

    if start == 0:
        start = time.time()

    end = time.time()    
    time_interval = end - start

    if beschleunigung_yout_skaliert < (0.25 * 9.8) and beschleunigung_yout_skaliert > (-0.25 * 9.8):
        pass
    else:
        speed = speed + (time_interval * beschleunigung_yout_skaliert)
        print "beschleunigung_yout: ", beschleunigung_yout_skaliert
        print "speed: ", speed

        s = str(beschleunigung_yout_skaliert)
        f.write(s)
        f.write(' ')
        
        t = t+time_interval
        t1 = str(t)
        f1.write(t1)
        f1.write(' ')
        
    start = end

    #print "beschleunigung_xout: ", ("%6d" % beschleunigung_xout), " skaliert: ", beschleunigung_xout_skaliert
