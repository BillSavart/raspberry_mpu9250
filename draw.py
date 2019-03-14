import cv2
import numpy as np

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

map_initiate()

