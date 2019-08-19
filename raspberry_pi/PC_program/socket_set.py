from windows import Ui_Form
from client_struct import client
import selectors
import socket
import numpy as np
import os
import sys
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtGui import *
from PyQt5.QtCore import QTimer, Qt
import cv2
import time
import keyboard
import types

class AppWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.initVar()
        self.img_map_loading()
        self.socket_initialize()

        self.timer=QTimer(self)
        self.timer.timeout.connect(self.update_image)
        self.timer.start(500)

        self.timer2 = QTimer(self)
        self.timer2.timeout.connect(self.get_socket_data)
        self.timer2.start(10)

        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.btn_info.clicked.connect(self.on_click_btn_info)
        self.ui.btn_map.clicked.connect(self.on_click_btn_map)
        self.ui.btn_image.clicked.connect(self.on_click_btn_image)
        self.ui.btn_choose.setEnabled(False)
        self.ui.btn_ok.setEnabled(False)     

        self.ui.label.setScaledContents(True)
        self.show()

    def initVar(self):
        self.image_image = np.zeros((800,800,3),np.uint8)
        self.image_map = np.zeros((800,800,3),np.uint8)
        self.image_info = np.zeros((800,800,3),np.uint8)
        self.keep = np.zeros((800,800,3),np.uint8)
        self.image = np.zeros((800,800,3),np.uint8)
        self.img_fireman = [ ]
        self.image_image_flag = False
        self.image_map_flag = True
        self.image_info_flag = False   
        self.middle_x = 1170
        self.middle_y = 700
        self.host = '192.168.68.100'
        self.port = 6666
        self.time_press = 0
        self.info_flag = 0
        self.client_list = [client(),client(),client(),client()]
        self.connection_num = np.zeros(4)
        self.subplot_count = [0, 1, 2, 3]
        self.client_dict = {"client":1}
        self.refresh_map = False
        self.refresh_img = False
        self.click_to_cancel = False
        self.name_space_height = 50 
        self.resize_height = 480+200
        self.resize_weight = 640+600
        self.height = 480
        self.weight = 640
        self.click_client = 0    ##### the client you click in window
        self.x_bound = 620   ##### window x axis bound
        self.y_bound = 340   ##### window y axis bound
#---------------------------------------------------------#
        self.inti_flag = -1
        self.init_time = 0
 
    def on_click_btn_info(self):
        self.image_image_flag = False
        self.image_map_flag = False
        self.image_info_flag = True
        self.ui.btn_choose.setEnabled(False)
        self.ui.btn_ok.setEnabled(False)

    def on_click_btn_map(self):
        self.image_image_flag = False
        self.image_map_flag = True
        self.image_info_flag = False
        self.ui.btn_choose.setEnabled(True)
        self.ui.btn_ok.setEnabled(True)

    def on_click_btn_image(self):
        self.image_image_flag = True
        self.image_map_flag = False
        self.image_info_flag = False
        self.ui.btn_choose.setEnabled(False)
        self.ui.btn_ok.setEnabled(False)     

    def update_image(self):
        image = self.image_map
        if(self.image_image_flag):
            image = self.image_image
        elif(self.image_map_flag):
            image = self.image_map
        elif(self.image_info_flag):
            image = self.image_info
        else:
            pass

#        cv2.imshow("Image",image)
#        cv2.waitKey(0)
        QIm = QImage(image.data, image.shape[1], image.shape[0],image.shape[1] *image.shape[2],QImage.Format_RGB888)
        self.ui.label.setPixmap(QPixmap.fromImage(QIm))

#    def mousePressEvent(self,event):
#        if(event.button() == Qt.LeftButton):
#            print("Left Mouse, x: ",event.pos().x())
#            print("Left Mouse, y: ",event.pos().y())

    def mousePressEvent(self,event):
        if(event.button() == Qt.LeftButton):
            if(self.image_map_flag):
                i = 0
                while(i<4):
                    if(self.connection_num[i] == 1 and self.client_list[i].position_x == 25 and self.client_list[i].position_y == 25):
                        self.client_list[i].position_x = event.pos().x()+150
                        self.client_list[i].position_y = event.pos().y()+150
                        print("x: ",self.client_list[i].position_x)
                        print("y: ",self.client_list[i].position_y)
                        break
                    elif(self.connection_num[i] == 1 and self.client_list[i].direction == -1):
                        if(abs(event.pos().x()+100 - self.client_list[i].position_x) > abs(event.pos().y()+95- self.client_list[i].position_y)):
                            if(event.pos().x()+100 > self.client_list[i].position_x):
                                self.client_list[i].direction = 90
                            else:
                                self.client_list[i].direction = 270
                        else:
                            if(event.pos().y()+95 > self.client_list[i].position_y):
                                self.client_list[i].direction = 180
                            else:
                                self.client_list[i].direction = 0
                        print("dir: ",self.client_list[i].direction)
                        break
                    else:
                        pass
                    i += 1
                print("Left Mouse, x: ",event.pos().x())
                print("Left Mouse, y: ",event.pos().y())
            else:
                pass
        else:
            pass

    def img_map_loading(self):
        fireman_img_map_path = "../IMAGE/fireman.png"
        map_img_map_path = "../IMAGE/1f.png"
        if(os.path.isfile(fireman_img_map_path)):
            print("Reading FireFighter Image...")
            while(len(self.img_fireman) == 0):
                self.img_fireman = cv2.imread(fireman_img_map_path)
            self.img_fireman = cv2.resize(self.img_fireman,(50,50))
            self.img_fireman = cv2.cvtColor(self.img_fireman,cv2.COLOR_RGB2BGR)
        else:
            print("There is no FireFighter Image")

        img_map = [] 
        print("Reading Environment Map...")
        if(os.path.isfile(map_img_map_path)):
            while(len(img_map) == 0):
                img_map = cv2.imread(map_img_map_path)
        print("Merge Map For Four FireFighters...")
        img_map = np.hstack((img_map,img_map))
        img_map = np.vstack((img_map,img_map))
 
        print("Drawing Security Line...")
        img_map = cv2.line(img_map,(5,5),(self.middle_x*2,5),(0,139,0),10,6)
        img_map = cv2.line(img_map,(5,self.middle_y),(self.middle_x*2,self.middle_y),(0,139,0),10,6)
        img_map = cv2.line(img_map,(5,self.middle_y*2),(self.middle_x*2,self.middle_y*2),(0,139,0),10,6)
        img_map = cv2.line(img_map,(5,5),(5,self.middle_y*2),(0,139,0),10,6)
        img_map = cv2.line(img_map,(self.middle_x,5),(self.middle_x,self.middle_y*2),(0,139,0),10,6)
        img_map = cv2.line(img_map,(self.middle_x*2,5),(self.middle_x*2,self.middle_y*2),(0,139,0),10,6)
 
        print("Set Initialize Map")
        self.keep = img_map.copy()
        self.image_map = img_map.copy()
        self.image = img_map.copy()

    def socket_initialize(self):    
        self.sel = selectors.DefaultSelector()
        lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        lsock.bind((self.host,self.port))
        lsock.listen()
        print('listening on', (self.host, self.port))
        lsock.setblocking(False)
        self.sel.register(lsock, selectors.EVENT_READ, data=None)
        print("Waiting For Connection...")


    def get_socket_data(self):
        if(keyboard.is_pressed('1') and time.time() - self.time_press > 1):
            self.time_press = time.time()
            self.info_flag = (self.info_flag != 0)*1 - 1
            print("pressed 1 , info_flag: ",self.info_flag)
        elif(keyboard.is_pressed('2') and time.time() - self.time_press > 1):
            self.time_press = time.time()
            self.info_flag = (self.info_flag != 1)*2 - 1
            print("pressed 2 , info_flag: ",self.info_flag)
        elif(keyboard.is_pressed('3') and time.time() - self.time_press > 1):
            self.time_press = time.time()
            self.info_flag = (self.info_flag != 2)*3 - 1
            print("pressed 3 , info _flag: ",self.info_flag)
        elif(keyboard.is_pressed('4') and time.time() - self.time_press > 1):
            self.time_press = time.time()
            self.info_flag = (self.info_flag != 3)*4 - 1
            print("pressed 4 , info_flag: ",self.info_flag)
        else:  
           pass
                 
        info_image = np.zeros((800,800,3),np.uint8)
         #---------------------------------#
        events = self.sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                self.accept_wrapper(key.fileobj)
            else:
                self.service_connection(key, mask)
                
                if(self.refresh_img or self.refresh_map or self.info_flag >= 0):
                    if(self.refresh_img):
                        self.refresh_img = False
                            ##### concate and plot image
                        img_concate_Hori=np.concatenate((self.client_list[0].img_read(),self.client_list[1].img_read()),axis=1)
                        img_concate_Verti=np.concatenate((self.client_list[2].img_read(),self.client_list[3].img_read()),axis=1)
                        img_toshow = np.concatenate((img_concate_Hori,img_concate_Verti),axis=0)
                        img_toshow = cv2.resize(img_toshow,(self.resize_weight,self.resize_height),interpolation=cv2.INTER_CUBIC)
                        self.image_image = img_toshow.copy()
                        #cv2.imshow(img_window_name,img_toshow)
                        #cv2.waitKey(1)
                    if(self.refresh_map):
                            #print("refresh map")
                        self.image_map = self.image.copy()
                        self.refresh_map = False
                            #-------------------------------------------------------------#
                            # to show image
 #                       cv2.imshow(map_window_name,image)
                            # Show 我們的圖
                            #-----------------------------------------------------------------#
                        ###
                    if(self.info_flag >= 0):
                        time_str = str(self.client_list[self.info_flag].time_pass)
                        time_str = time_str.partition('.')[0]+"."+time_str.partition('.')[2][0:1]
                        cv2.putText(info_image,"Name: "+str(self.client_list[self.info_flag].name), (10, 40), cv2.FONT_HERSHEY_SIMPLEX,1, (255, 255, 0), 1, cv2.LINE_AA)
                        cv2.putText(info_image,"Number: "+str(self.client_list[self.info_flag].fire_num), (10, 80), cv2.FONT_HERSHEY_SIMPLEX,1, (255, 255, 0), 1, cv2.LINE_AA)
                        cv2.putText(info_image,' '.join(["Time Pass:",time_str,"secs"]), (10, 120), cv2.FONT_HERSHEY_SIMPLEX,1, (255, 255, 0), 1, cv2.LINE_AA)
                        self.image_info = info_image.copy()
#                        cv2.imshow(info_window_name,info_image)                        
                        ###
                   
#                    if cv2.waitKey(1) & 0xFF == ord('q'):
#                        break
                    if(self.click_to_cancel):
                        self.set_namespace_color(click_client,(255,255,255),(0, 0, 0))
                        self.client_list[click_client].set_sos_flag(False)
                        self.click_to_cancel = False
 
    def accept_wrapper(self,sock):
        conn, addr = sock.accept()  # Should be ready to read
        print('accepted connection from', addr)
    
        conn.setblocking(False)
        data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self.sel.register(conn, events, data=data)
        ##### create an client object an put into dictionary with it's address
        min_num = min(self.subplot_count)
        ##### create an white img with client name
        self.client_list[min_num]=client()
        self.client_dict[str(addr[1])] = min_num
        ##### number remove from list subplot_count
        self.subplot_count.remove(min_num)
    
        #--------------------------------------------------------------#
        i = 0                                                             
        while(i<4):
            if(self.connection_num[i] == 0):
                self.client_list[i].set_info(i,str(addr[0]))
                self.connection_num[i] = 1
                inti_flag = i
                break
            i = i + 1
    # add new connection
    # 創造一個新的Object給Device
#--------------------------------------------------------------------#
    
        print("Client: ")
        print("\tnum: ",self.client_list[i].id_num)
        print("\tip_addr: ",self.client_list[i].ip_addr)
    
 
    def set_namespace_color(self,client_index,background_color,font_color):
        namespace_whiteimg = np.zeros((self.name_space_height,self.weight,3), np.uint8)
        namespace_whiteimg[:,:] = background_color
        name = self.client_list[client_index].get_name()
        cv2.putText(namespace_whiteimg, name, (200, 42), cv2.FONT_HERSHEY_SIMPLEX, 2, font_color, 3, cv2.LINE_AA)
        self.client_list[client_index].namespace_imgset(namespace_whiteimg)
 
    def service_connection(self,key, mask):
        sock = key.fileobj
        data = key.data
        if mask & selectors.EVENT_READ:
            recv_data = None
            client_host = self.client_dict[str(data.addr[1])]
            if(self.client_list[client_host].first_time_recv()):
                print("Getting Name...")
                recv_data = sock.recv(16)
                name = recv_data.decode()
                #name = (str)(client_list[client_host].get_num()) + "." + name
                self.client_list[client_host].set_name(name)
                ##### Default : white background black font
                self.set_namespace_color(client_host,(255,255,255),(0, 0, 0))   
                print("The Name is: ",name)
                self.init_time = time.time() 
            else:
                if(self.client_list[client_host].package_size() < 0):
                    try:
                        ##### recv the img size
                        recv_data = sock.recv(16)
                        recv_data_msg = recv_data.decode().strip()
                        if("SIZE" in recv_data_msg):
                            #print("image size msg")
                            self.client_list[client_host].package_set(int(recv_data_msg[4:len(recv_data_msg)]))
                        else:
                            #------------------------------------------------------------------#
                            for i in self.client_list:
                                if(i.ip_addr == str(data.addr[0])):
                                    i.time_pass = time.time() - self.init_time
                                    #print(i.time_pass)
                                    if("HELP2" in recv_data_msg):
                                        print("HELP2")
                                        self.helpConditionExec("HELP2",i.id_num)
                                        self.client_list[client_host].set_sos_flag(True)
                                        sock.send("I will save you".encode())
                                    elif("HELP" in recv_data_msg):
                                        print("HELP")
                                        self.helpConditionExec("HELP",i.id_num)
                                    elif("num" in recv_data_msg):
                                        i.fire_num = recv_data_msg[3:len(recv_data_msg)]
                                        #print(i.fire_num)
                                    else:
                                        print("id: ",i.id_num)
                                        print(recv_data_msg)
                                        self.drawNewSpot(recv_data_msg,i.id_num,self.img_fireman)                    
                                    break
                                # Device 傳輸資料時, call 對應function
                            #--------------------------------------------------------------------#
                    except Exception as e:
                        print (e.args)
                else:
                    ##### recv the img
                    #print("image msg")
                    recv_data = sock.recv(client_list[client_host].package_size())
                    ##### concatenate recv msg to img
                    self.client_list[client_host].img_combine(recv_data)
                    self.client_list[client_host].package_decrease(len(recv_data))
                    if(self.client_list[client_host].package_size() <= 0):
                        ##### img recv complete
                        self.client_list[client_host].img_decode()
                        self.client_list[client_host].package_set(-1)
                        self.refresh_img = True
                        ##### decide which background color to brush
                        brush_background_ornot = self.client_list[client_host].brush_background()
                        if(brush_background_ornot == 1):
                            ##### Red background white font
                            self.set_namespace_color(client_host,(0,0,255),(255, 255, 255))
                        elif (brush_background_ornot == 2):
                            ##### White background black font
                            self.set_namespace_color(client_host,(255,255,255),(0, 0, 0))
                    #except Exception as e:
                    #    print(e.args)
 
            if not recv_data:
                print('closing connection to', data.addr)
                #-------------------------------------------------------------------#
                print(str(data.addr[0]))
                print(self.client_list[0].ip_addr)
                for i in client_list:
                    if(i.ip_addr == str(data.addr[0])):
                        self.connection_num[i.id_num] = 0
                self.refresh_map = True
                # Close Connection 的時候取消 Object
                #--------------------------------------------------------------------#
                self.client_list[client_dict[str(data.addr[1])]].set_visible(False)
                self.refresh_img = True
                self.subplot_count.append(client_dict[str(data.addr[1])])
                del self.client_dict[str(data.addr[1])]
                self.sel.unregister(sock)
                sock.close()

    def drawNewSpot(self,data,index,img_fireman):
        self.image = self.keep.copy()
 
        left_spot_x = 5 + (self.middle_x-5)*(index%2)
        right_spot_x = self.middle_x + self.middle_x*(index%2)
        up_spot_y = 5 + (self.middle_y-5)*(index >= 2)
        down_spot_y = self.middle_y + (self.middle_y)*(index >= 2)
 
        self.client_list[index].color_set = (0,139,0)
        cv2.line(self.image,(left_spot_x,up_spot_y),(right_spot_x,up_spot_y),self.client_list[index].color_set,10,6)
        cv2.line(self.image,(left_spot_x,down_spot_y),(right_spot_x,down_spot_y),self.client_list[index].color_set,10,6)
        cv2.line(self.image,(left_spot_x,up_spot_y),(left_spot_x,down_spot_y),self.client_list[index].color_set,10,6)
        cv2.line(self.image,(right_spot_x,up_spot_y),(right_spot_x,down_spot_y),self.client_list[index].color_set,10,6)
 
        if("No Turn" in data):
             #print("index:",index)
            self.client_list[index].addNewPosition("No Turn",0)
        elif("Left" in data):
            self.client_list[index].addNewPosition("Left",0)
        elif("Right" in data):
            self.client_list[index].addNewPosition("Right",0)
        else:
            self.client_list[index].addNewPosition("No Turn",float(data))
        self.refresh_map = True
        #print('refresh')
        print("lalax: ",self.client_list[0].position_x)
        print("lalay: ",self.client_list[0].position_y)
        for i in range(4):
            self.image[self.client_list[i].position_y-25 : self.client_list[i].position_y + 25 ,self.client_list[i].position_x-25 : self.client_list[i].position_x + 25] = img_fireman
 
    def helpConditionExec(self,message,index):
        if("HELP2" in message):
            self.client_list[index].color_set = (255,0,0)
        elif("HELP" in message):
            self.client_list[index].color_set = (255,165,0)
        else:
            pass
 
        left_spot_x = 5 + (self.middle_x-5)*(index%2)
        right_spot_x = self.middle_x + self.middle_x*(index%2)
        up_spot_y = 5 + (self.middle_y-5)*(index >= 2)
        down_spot_y = self.middle_y + (self.middle_y)*(index >= 2)
 
        cv2.line(self.image,(left_spot_x,up_spot_y),(right_spot_x,up_spot_y),self.client_list[index].color_set,10,6)
        cv2.line(self.image,(left_spot_x,down_spot_y),(right_spot_x,down_spot_y),self.client_list[index].color_set,10,6)
        cv2.line(self.image,(left_spot_x,up_spot_y),(left_spot_x,down_spot_y),self.client_list[index].color_set,10,6)
        cv2.line(self.image,(right_spot_x,up_spot_y),(right_spot_x,down_spot_y),self.client_list[index].color_set,10,6)
    
        self.refresh_map = True


app = QApplication(sys.argv)
w = AppWindow()
w.show()
sys.exit(app.exec_())
