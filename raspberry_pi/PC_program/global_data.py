import cv2
import numpy as np
from client_struct import client

keep = []
image_image = []
image_map = []
image_info = []
image_image_flag = False
image_map_flag = False
image_info_flag = False
client_list = [client(),client(),client(),client()]

def intialize():
    global image_image
    global image_map
    global image_info
    image_image = cv2.imread('../IMAGE/1f.png')  
    image_map = cv2.imread('../IMAGE/5f.png')    
    image_info = np.zeros((800,800,3), np.uint8)

def img_map_loading():
    global keep
    fireman_img_map_path = "../IMAGE/fireman.png"
    map_img_map_path = "../IMAGE/1f.png"
    if(os.path.isfile(fireman_img_map_path)):
        print("Reading FireFighter Image...")
        while(len(img_fireman) == 0):
            img_fireman = cv2.imread(fireman_img_map_path)
        img_fireman = cv2.resize(img_fireman,(50,50))
    else:
        print("There is no FireFighter Image")
             
    print("Reading Environment Map...")
    if(os.path.isfile(map_img_map_path)):
        while(len(img_map) == 0):
            img_map = cv2.imread(map_img_map_path)
    print("Merge Map For Four FireFighters...")
    img_map = np.hstack((img_map,img_map))
    img_map = np.vstack((img_map,img_map))
             
    print("Drawing Security Line...")
    img_map = cv2.line(img_map,(5,5),(middle_x*2,5),(0,139,0),10,6)
    img_map = cv2.line(img_map,(5,middle_y),(middle_x*2,middle_y),(0,139,0),10,6)
    img_map = cv2.line(img_map,(5,middle_y*2),(middle_x*2,middle_y*2),(0,139,0),10,6)
    img_map = cv2.line(img_map,(5,5),(5,middle_y*2),(0,139,0),10,6)
    img_map = cv2.line(img_map,(middle_x,5),(middle_x,middle_y*2),(0,139,0),10,6)
    img_map = cv2.line(img_map,(middle_x*2,5),(middle_x*2,middle_y*2),(0,139,0),10,6)
             
    print("Set Initialize Map")
    keep = img_map.copy()
    global_data.image_map = img_map.copy()
