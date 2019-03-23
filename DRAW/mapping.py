import cv2
import numpy as np
import time

inti_flag = False
position_x = 0
position_y = 0
direction = -1

def positionInitiate(event,x,y,flags,param):
    global position_x
    global position_y
    global inti_flag
    global direction

    if  event == cv2.EVENT_LBUTTONDOWN and (direction == -1 or inti_flag == False):    
        if inti_flag == False:
            position_x = x
            position_y = y
            print "x: ",x
            print "y: ",y
            inti_flag = True
        else:
            temp_x = x
            temp_y = y
            if abs(temp_x-position_x) > abs(temp_y - position_y):
                if temp_x < position_x:
                    direction = 270
                else:
                    direction = 90
            else:
                if temp_y > position_y:
                    direction = 180
                else:
                    direction = 0
            print "dir: ",direction

def addNewPosition(direct,dist):
    global inti_flag
    global direction
    global position_x
    global position_y

    if inti_flag == True:
# change direction        
        if direct == "right":
            direction += 90
            if direction >= 360:
                direction -= 360
        elif direct == "left":
            direction -= 90
            if direction < 0:
                direction += 360
        else:
            pass #no direction changes

#change distance
        dist_cm = dist*100 # change meter to centimeter
        map_cm = dist_cm/320 # change the billy ruler
        pixel_num = int(map_cm*100/1.5) # change to pixel
        
        if direction == 0:
            position_y += pixel_num
        elif direction == 90:
            position_x -= pixel_num
        elif direction == 180:
            position_y -= pixel_num
        elif direction == 270:
            position_x += pixel_num
        else:
            pass


def main():
    global position_x
    global position_y

    image = cv2.imread("../IMAGE/image_draw.JPG")
    cv2.namedWindow("Image")
    cv2.setMouseCallback('Image',positionInitiate)
    cv2.imshow("Image",image)
    cv2.waitKey(0)

    while(True):
        cv2.circle(image,(position_x,position_y),3,(255,255,255),5)
        addNewPosition("right",5)
        cv2.circle(image,(position_x,position_y),3,(0,0,0),5)
        cv2.imshow("Image",image)
        if cv2.waitKey() == ord('q'):
            break



if __name__ == "__main__" :
    main()
