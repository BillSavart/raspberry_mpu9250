import cv2
import numpy as np
import time

inti_flag = False
position_x = 0
position_y = 0
move_distance = 0
direction = "None"
move_direction = "None"

def positionInitiate(event,x,y,flags,param):
    global position_x
    global position_y
    global inti_flag

    if inti_flag == False and event == cv2.EVENT_LBUTTONDOWN:
        inti_flag = True    
        position_x = x
        position_y = y
        print "x: ",x
        print "y: ",y

def addNewPosition():
    global inti_flag
    if inti_flag == True:
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
        addNewPosition()
        cv2.circle(image,(position_x,position_y),3,(255,255,255),10)
        cv2.imshow("Image",image)
        time.sleep(1)
        if cv2.waitKey() == ord('q'):
            break



if __name__ == "__main__" :
    main()
