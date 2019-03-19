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

# 1:320 for map information
bus = smbus.SMBus(1) # bus = smbus.SMBus(0) fuer Revision 1
address = 0x68       # via i2cdetect
bus.write_byte_data(address, power_mgmt_1, 0)  #initiate mpu6500
bus.write_byte_data(address, 0x37, 0x02) #initiate bypass

mag_address = 0x0c
bus.write_byte_data(mag_address, 0x0A, 0b0110) #initiate AKB8963

# list for low pass filter
bes_arr = []
time_arr = []

#
min_num = -0.3
max_num = 0.2
sample_num = 500

# low pass filter 
order = 3
Wn = 0.003
b,a = signal.butter(order, Wn, 'low')

distance = 0
velocity = 0

velocity_f = open("vfile.txt","w")
time_f = open("time.txt","w")
time_total = 0
dis_f = open("d_file.txt","w")
acc_f = open("a_file.txt","w")
acc_lf = open("al_file.txt","w")

while True:
    time_temp = time.time()
    time_arr.append(time_temp)

    bes_x = read_word_2c(0x3b, address)
    bes_y = read_word_2c(0x3d, address)
    bes_z = read_word_2c(0x3f, address)

    bes_y_ska = bes_y / 16384.0 * 9.8

    time_total  = time_total + time_temp
    time_f.write(str(time_total))
    time_f.write(" ")

    if len(bes_arr) == sample_num:
        lfilt = signal.lfilter(b, a, bes_arr)
        lfilt = signal.lfilter(b, a, lfilt)
        if max(lfilt) < max_num and min(lfilt) > min_num:
            for i in lfilt:
                acc_lf.write("0 ")
        else:
            i = 1
            acc_lf.write(str(lfilt[0]))
            acc_lf.write(" ")
            while i < sample_num:
                acc_lf.write(str(lfilt[i]))
                acc_lf.write(" ")
                if lfilt[i] < max_num and lfilt[i] > min_num:
                    pass
                else:
                    distance = distance + velocity*(time_arr[i]-time_arr[i-1])+0.5*lfilt[i]*(time_arr[i]-time_arr[i-1])*(time_arr[i]-time_arr[i-1])
                    velocity = velocity + lfilt[i]*(time_arr[i]-time_arr[i-1])
                i = i + 1
        bes_arr = []
        time_arr = []
        print "distance: " , distance
        velocity_f.write(str(velocity))
        velocity_f.write(" ")
        dis_f.write(str(distance))
        dis_f.write(" ")
        acc_f.write(str(bes_y_ska))
        acc_f.write(" ")
    else:
        velocity_f.write(str(velocity))
        velocity_f.write(" ")
        dis_f.write(str(distance))
        dis_f.write(" ")
        bes_arr.append(bes_y_ska)
        acc_f.write(str(bes_y_ska))
        acc_f.write(" ")
        
