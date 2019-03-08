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
address = 0x68
bus.write_byte_data(address, power_mgmt_1, 0)
bus.write_byte_data(address, 0x37, 0x02)

address = 0x0c       # via i2cdetect
bus.write_byte_data(address, 0x0A, 0b0110)

f = open('make_record.txt','w')
f1 = open('make_time.txt','w')

t = 0

# Aktivieren, um das Modul ansprechen zu koennen
#bus.write_byte_data(address, power_mgmt_1, 0) 

start = 0
end = 0
prev = 0
now = 0

while True:
    mag_xout = read_word_2c(0x04)
    mag_yout = read_word_2c(0x06)
    mag_zout = read_word_2c(0x08)

    if prev == 0:
        prev = mag_yout
        start = time.time()
    end = time.time()
    now = mag_yout
    
    print prev
    print now
#    if prev-now <= 10 and prev-now >= -10:
   #     print "prev: ", prev
    #    print "now: ", now
 #       print "no move"
      #  pass
 #   else:
 #       print "Move\n"
 #       prev = now
    
    time_inter = end-start
    t += time_inter
    s1 = str(t)
    f1.write(s1)
    f1.write(' ')
    s = str(now)
    f.write(s)
    f.write(' ')

    i=300000
    j=300000
    while(i!=0):
        while(j!=0):
            j=j-1
        i=i-1

    prev = now
    start = end

    #print mag_xout
    #print mag_yout
    #print mag_zout
