import cv2

class StructureConnection:
    color_set = (0,0,0) # 紅綠燈的燈號
    id_num = 0 # 顯示在Map的數字
    ip_addr = "" # 裝置ip
    position_x = 0 # 裝置在Map的位置(x)
    position_y = 0 # 裝置在Map的位置(y)
    direction = -1 # 裝置方向
    dist_save = 0 # 距離暫存
  
    def __init__(self,num,ip_position): # Constructor
        self.color_set = (0,255,0)
        self.id_num = num
        self.ip_addr = ip_position

    def addNewPosition(self,direct,dist,image): # 我們的function
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
                print(direct) 
#change distance
            print(self.direction)
            dist = dist + self.dist_save # avoid error
            dist_cm = dist*100 # change meter to centimeter
            if dist_cm < 320:
                self.dist_save = self.dist_save + dist
            else:
                self.dist_save = 0
                map_cm = dist_cm/320 # change the billy ruler
                pixel_num = int(map_cm*100/1.5) # change to pixel
                print("pixel_num: "+str(pixel_num)) 
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


