import numpy as np
import cv2
import struct

height = 480
weight = 640
name_space_height = 50

img_white = np.zeros((height+name_space_height,weight,3), np.uint8)
img_white[:,:] = (255,255,255)

img_white_namespace = np.zeros((name_space_height,weight,3), np.uint8)
img_white_namespace[:,:] = (255,255,255)

matrix = np.loadtxt("matrix6.txt", delimiter=',')
M = cv2.getRotationMatrix2D((weight/2,height/2), 180, 1)

class client:
    th_70 = 0   ###### threshold for 70 degree flir value
    th_100 = 0  ###### threshold for 100 degree flir value
    remain_package_size = 0
    img_binary = b''
    img_ir = img_white
    img_combine = img_white
    img_show = img_white    
    name = "name"
    recv_ir_flag = False
    recv_flir_flag = False
    visible_flag = False
    first_flag = False  ###### first time recv msg
    sos_flag = False
    twinkling_flag = False
    closing_danger_flag = False     ###### close to the danger area
    in_danger_flag = False      ###### the red area more than one third of pic
# ---------------------------------------------#
    color_set = (0,0,0) # 紅綠燈的燈號
    fire_num = ""
    fire_name = ""
    time_pass = 0
    id_num = 0 # 顯示在Map的數字
    ip_addr = "" # 裝置ip
    ip_addr_num = 0
    position_x = 25 # 裝置在Map的位置(x)
    position_y = 25 # 裝置在Map的位置(y)
    direction = -1 # 裝置方向
    dist_save = 0 # 距離暫存
    bes_data_list = []
    gyro_list = []
#------------------------------------------------#
    def __init__(self):
        self.visible_flag = True
        self.first_flag = True
        self.namespace_img = img_white_namespace

    def set_info(self, num, ip_position):
        self.id_num = num
        self.ip_addr = ip_position
        self.color_set = (0,255,0)

    def set_threshold(self, th70_or_100, num):
        if(th70_or_100 == 1):
            ###### set the 70 degree threshold of flir value ######
            self.th_70 = num
        else:
            ###### set the 100 degree threshold of flir value ######
            self.th_100 = num

    def set_close_danger(self, flag):
        self.closing_danger_flag = flag

    def set_namespace(self, my_namespace_img):
        ###### set the image with name ######
        self.first_flag = False
        self.namespace_img = my_namespace_img

    def set_sos_flag(self, flag):
        self.sos_flag = flag

    def brush_namespace_background(self):
        if(self.sos_flag):
            if(self.twinkling_flag):
                self.twinkling_flag = False
                return 1    ###### red background
            else:
                self.twinkling_flag = True
                return 2    ###### white background
        return 0    ###### do not need to brush background

    def first_time_recv(self):
        return self.first_flag

    def set_visible(self, flag):
        self.visible_flag = flag

    def set_name(self, myname):
        self.name = myname

    def get_name(self):
        return self.name
        
    def get_package_size(self):
        return self.remain_package_size

    def set_package(self, package_num, ir_or_flir):
        self.remain_package_size = package_num
        if(ir_or_flir == 1):
            self.recv_ir_flag = True
        elif(ir_or_flir == 2):
            self.recv_flir_flag = True
        else:
            self.recv_ir_flag = False
            self.recv_flir_flag = False

    def decrease_package_size(self, num):
        self.remain_package_size -= num

    def combine_recv_img(self,recv_str):
        self.img_binary += recv_str
    
    def read_img(self):
        if(self.visible_flag):
            return_img = self.img_show
        else:
            return_img = img_white
        return return_img

    def read_combine_img(self):
        return self.img_combine

    def decode_img(self):
        try:
            if(self.recv_ir_flag):
                ###### decode ir image ######
                self.recv_ir_flag = False
                data = np.fromstring(self.img_binary, dtype = 'uint8')
                data = cv2.imdecode(data, 1)
                self.img_binary = b''
                self.img_ir = np.reshape(data, (height, weight, 3))
                return False
            elif(self.recv_flir_flag):
                ###### decode flir value ######
                self.recv_flir_flag = False
                data = struct.unpack("4800I", self.img_binary)
                self.img_binary = b''
                data = (np.asarray(data)).astype(np.float32)
                data = np.reshape(data, (60,80,1))
                ###### if over threshold, replace part of ir image with red or green color ######
                dst = cv2.resize(data, (weight,height), interpolation= cv2.INTER_CUBIC)
                dst = np.dstack([dst]*3)
                tmp = self.img_ir.copy()
                dst = cv2.warpPerspective(dst,matrix, (weight,height))
                np.place(tmp, (dst > self.th_100), (0,0,255))
                np.place(tmp, ((dst > self.th_70)&(dst <= self.th_100)), (163,255,197))
                before_rotate_img = cv2.addWeighted(self.img_ir, 0.5, tmp, 0.5, 0)
                ###### rotate image ######
                rotate_img = cv2.warpAffine(before_rotate_img, M, (weight,height))
                self.img_combine = rotate_img
                ###### put the warning message on pic ######
                if(np.sum((data> self.th_100)) >= (data.size / 3)):
                    print("sum= ",np.sum((data> self.th_100)),"size= ",data.size)
                    ###### if the red area more one third of pic, rise the in_danger_flag ######
                    self.in_danger_flag = True
                    cv2.putText(self.img_combine, "In danger area !", (20,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 3)
                elif(self.closing_danger_flag):
                    cv2.putText(self.img_combine, "Close to danger area", (20,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 3)
                    self.closing_danger_flag = False
                ###### concatenate the img_combine and namespace ######
                self.img_show = np.concatenate((self.namespace_img, self.img_combine), axis=0)
                return True
            return False

        except Exception as e:
            print(e.args)
            ###### if decode image fail, show the white image ######
            self.img_show = img_white
            return False
        return False

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

