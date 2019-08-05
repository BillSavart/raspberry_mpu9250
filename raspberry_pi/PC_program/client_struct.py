import numpy as np
import cv2
height = 480
weight = 640
name_space_height = 50

white_img = np.zeros((height+name_space_height,weight,3), np.uint8)
white_img[:,:] = (255,255,255)

namespace_whiteimg = np.zeros((name_space_height,weight,3), np.uint8)
namespace_whiteimg[:,:] = (255,255,255)

class client:
    remain_package_size = -1
    binary_img = b''
    subplot_number = 0
    img = white_img
    visible = False
    first = False
    sos_flag = False
    twinkling = False
    name = "name"
# ---------------------------------------------#
    color_set = (0,0,0) # 紅綠燈的燈號
    fire_num = ""
    fire_name = ""
    time_pass = 0
    id_num = 0 # 顯示在Map的數字
    ip_addr = "" # 裝置ip
    position_x = 25 # 裝置在Map的位置(x)
    position_y = 25 # 裝置在Map的位置(y)
    direction = -1 # 裝置方向
    dist_save = 0 # 距離暫存
    bes_data_list = []
    gyro_list = []
#------------------------------------------------#
    def __init__(self):
        self.visible = True
        self.namespace_img = namespace_whiteimg
        self.first = True

    def set_info(self,num,ip_position):
        self.id_num = num
        self.ip_addr = ip_position
        self.color_set = (0,255,0)

    def namespace_imgset(self,my_namespace_img):
        self.namespace_img = my_namespace_img
        self.first = False

    def set_sos_flag(self,flag):
        self.sos_flag = flag

    def brush_background(self):
        if(self.sos_flag):
            if(self.twinkling):
                self.twinkling = False
                return 1    ##### red background
            else:   
                self.twinkling = True
                return 2    ##### white background
            return 0    ##### do not need to brush background

    def first_time_recv(self):
        return self.first

    def set_visible(self,tORf):
        self.visible = tORf

    def set_name(self,myname):
        self.name = myname

    def get_name(self):
        return self.name
    '''
    def get_num(self):
        return self.num
    '''
    def package_size(self):
        return self.remain_package_size

    def package_set(self,package_num):
        self.remain_package_size = package_num

    def package_decrease(self, decrease_num):
        self.remain_package_size -= decrease_num

    def img_combine(self,recv_str):
        self.binary_img += recv_str
    
    def img_read(self):
        if(self.visible):
            return_img = self.img
        else:
            return_img = white_img
        return return_img

    def img_decode(self):
        ##### decode the string and turn to 2 dimension array
        try:
            data = np.fromstring(self.binary_img, dtype = 'uint8')
            data = cv2.imdecode(data,1)
            self.binary_img = b''
            self.img = np.reshape(data,(height,weight,3))
            self.img = np.concatenate((self.namespace_img,self.img),axis=0)
        except:
            self.img = white_img

    def addNewPosition(self,direct,dist): # 我們的function
        if self.direction != -1:
# change direction        
            if direct == "Right":
                self.dist_save = 0
                self.direction += 90
                if self.direction >= 360:
                    self.direction -= 360
            elif direct == "Left":
                self.dist_save = 0
                self.direction -= 90
                if self.direction < 0:
                    self.direction += 360
            elif direct == "No Turn" or direct == "":
                pass #no direction changes
            else:
                pass
                #print(direct)
#change distance
            #print(self.direction)
            dist = dist + self.dist_save # avoid error
            dist_cm = dist*100 # change meter to centimeter
            if dist_cm < 70:
                self.dist_save = self.dist_save + dist
            else:
                self.dist_save = 0
                map_cm = dist_cm/228.69 # change the billy ruler
                pixel_num = int(map_cm*100/1.5) # change to pixel
                #print("pixel_num: "+str(pixel_num))
                if self.direction == 0:
                    self.position_y -= pixel_num
                elif self.direction == 90:
                    self.position_x += pixel_num
                elif self.direction == 180:
                    self.position_y += pixel_num
                elif self.direction == 270:
                    self.position_x -= pixel_num
                else:
                    pass

