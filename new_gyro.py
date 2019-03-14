#!/usr/bin/python
import smbus
import math
import time
import cv2
import numpy as np

# Register
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c
 
# Image

image = cv2.imread("indoor_position.JPG", 1)
canny = image
image_draw = image

mouse_start_x = 0
mouse_start_y = 0
mouse_end_x = 0
mouse_end_y = 0
mouse_door_start_x = 0
mouse_door_start_y = 0
mouse_door_end_x = 0
mouse_door_end_y = 0
mouse_flag = False
mouse_stop_flag = True
mouse_dbl_clk_flag = False
mouse_draw_flag = True

def set_image(event, x, y, flags, param):
    global mouse_start_x
    global mouse_start_y
    global mouse_end_x
    global mouse_end_y
    global mouse_flag
    global mouse_dbl_clk_flag
    global mouse_door_start_x
    global mouse_door_start_y
    global mouse_door_end_x
    global mouse_door_end_y
    global mouse_draw_flag

    if event == cv2.EVENT_LBUTTONDOWN and mouse_draw_flag == True:
        if mouse_flag == False:
            mouse_flag = True
            mouse_start_x = x
            mouse_start_y = y
        else:
            mouse_end_x = x
            mouse_end_y = y
            cv2.line(image_draw, (mouse_start_x, mouse_start_y), (mouse_end_x, mouse_end_y), (0, 0, 255), 4)
            mouse_start_x = mouse_end_x
            mouse_start_y = mouse_end_y
            print("line")
    elif event == cv2.EVENT_LBUTTONDBLCLK and mouse_draw_flag == True:
        print("door")
        if mouse_dbl_clk_flag == False:
            mouse_flag = False
            mouse_door_start_x = x
            mouse_door_start_y = y
            mouse_dbl_clk_flag = True
        else:
            mouse_door_end_x = x
            mouse_door_end_y = y
            cv2.line(image_draw, (mouse_door_start_x, mouse_door_start_y), (mouse_door_end_x, mouse_door_end_y), (255, 0, 0), 4)
            mouse_dbl_clk_flag = False
    elif event == cv2.EVENT_RBUTTONDOWN:
        cv2.imwrite("image_draw.JPG",image_draw)
        mouse_draw_flag = False

def map_initiate():
    G_image = cv2.GaussianBlur(image, (3, 3), 0)
    canny = cv2.Canny(G_image, 50, 150)

    cv2.namedWindow("Image")
    cv2.setMouseCallback('Image', set_image)
    
    height, weight,channel = image_draw.shape
    for x in range(0,height):
        for y in range(0,weight):
            image[x][y]=255

    cv2.imshow("Image", canny)
    cv2.waitKey(0)

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
 
# Aktivieren, um das Modul ansprechen zu koennen
bus.write_byte_data(address, power_mgmt_1, 0)

start = 0
end = 0

sum_r = 0
sum_l = 0

map_initiate()

while True:
 #   print "Gyroskop"
#    print "--------"
    break

    if start == 0:
        start = time.time()

    end = time.time()
    #time_interval = end - start - 1
    time_interval = end - start

    gyroskop_xout = read_word_2c(0x43)
    gyroskop_yout = read_word_2c(0x45)
    gyroskop_zout = read_word_2c(0x47)

#    print "time_inter: ", time_interval

    x_out = gyroskop_xout * 250 * time_interval / 131
#    y_out = gyroskop_yout * 250 * time_interval / 131
 #   z_out = gyroskop_zout * 250 * time_interval / 131

    if x_out > -4 and x_out < 4:
        x_out = 0

    if x_out == 0:
    #    sum_r = 0
     #   sum_l = 0
      #  print "sum_r: ", sum_r
       # print "sum_l: ", sum_l
        pass
    elif x_out > 0:
        sum_l = 0
        sum_r = sum_r + x_out
 #       print "sum_r: ", sum_r
#        print "sum_l: ", sum_l
        if sum_r > 18000:
            print "sum_r: ", sum_r
            print "sum_l: ", sum_l
            sum_r = 0
            print "Turn Right"
    else:
        sum_r = 0
        sum_l = sum_l + x_out
   #     print "sum_r: ", sum_r
  #      print "sum_l: ", sum_l
        if sum_l < -18000:
            print "sum_r: ", sum_r
            print "sum_l: ", sum_l
            sum_l = 0
            print "Turn Left"
     
    #if x_out < -4 or x_out > 4:
     #   print "x_out: ", x_out
   # if y_out < -4 or y_out > 4:
    #    print "y_out: ", y_out
    #if z_out < -4 or z_out > 4:
     #   print "z_out: ", z_out
    
   # print "gyroskop_xout: ", ("%5d" % gyroskop_xout), " skaliert: ", (gyroskop_xout / 131)
   # print "gyroskop_yout: ", ("%5d" % gyroskop_yout), " skaliert: ", (gyroskop_yout / 131)
   # print "gyroskop_zout: ", ("%5d" % gyroskop_zout), " skaliert: ", (gyroskop_zout / 131)

    #print
    start = end
    time.sleep(1)
