import smbus
import math
import time

power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

def read_byte(reg):
    return bus.read_byte_data(address,reg)

def read_word(reg):
    h = bus.read_byte_data(address,reg)
    l = bus.read_byte_data(address,reg)
    value = (h << 8) + l
    return value

def read_word_2c(reg):
    val = read_word(reg)
    if(val >= 0x8000):
        return -((65535-val)+1)
    else:
        return val

def dist(a,b):
    return math.sqrt((a*a)+(b*b))

def get_y_rotation(x,y,z):
    radians = math.atan2(x,dist(y,z))
    return -math.degrees(radians)

def get_x_rotation(x,y,z):
    radians = math.atan2(y,dist(x,z))
    return math.degrees(radians)

bus = smbus.SMBus(1)
address = 0x68

bus.write_byte_data(address,power_mgmt_1,0)

while (True):
    print "Gyroskop"
    print "--------"

    gyroskop_xout = read_word_2c(0x43)
    gyroskop_yout = read_word_2c(0x45)
    gyroskop_zout = read_word_2c(0x47)

    print "gyroskop_xout: ", (gyroskop_xout/131)
    print "gyroskop_yout: ", (gyroskop_yout/131)
    print "gyroskop_zout: ", (gyroskop_zout/131)

    print
    print "Beschleunigungssensor"
    print "---------------------"

    beschleunigung_xout = read_word_2c(0x3b)
    beschleunigung_yout = read_word_2c(0x3d)
    beschleunigung_zout = read_word_2c(0x3f)

    beschleunigung_xout_ska = beschleunigung_xout/16384.0
    beschleunigung_yout_ska = beschleunigung_yout/16384.0
    beschleunigung_zout_ska = beschleunigung_zout/16384.0

    print "beschleunigung_xout: ",(beschleunigung_xout_ska)
    print "beschleunigung_yout: ",(beschleunigung_yout_ska)
    print "beschleunigung_zout: ",(beschleunigung_zout_ska)

    print "X Rotation: ", get_x_rotation(beschleunigung_xout_ska,beschleunigung_yout_ska,beschleunigung_zout_ska)
    print "Y Rotation: ",get_y_rotation(beschleunigung_xout_ska,beschleunigung_yout_ska,beschleunigung_zout_ska)

    time.sleep(1)
