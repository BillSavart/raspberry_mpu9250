import cv2
import numpy as np



inti_flag = False
position_x = 0
position_y = 0
move_distance = 0
direction = "None"
move_direction = "None"


def positionInitiate(event,x,y,flags,param):
    if inti_flag==False:
        inti_flag = True
        if event == cv2.EVENT_LBUTTONDOWN:
            posiotion_x = x
            positiony_y = y


def addNewPosition():
    pass


def main():
    image = cv2.imread()
if __name__ == "__main__" :
    main()
