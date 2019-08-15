import selectors
import socket
import types
import numpy as np
import cv2
from client_struct import client
import time
import keyboard
import os
import time

##### socket connection: use "ifconfig" to find your ip
host = '192.168.68.100'
#host = '192.168.208.108'
port = 6666

##### windows defined
img_window_name = 'Firefighter' # image_window_name
map_window_name = 'Map'
info_window_name = 'Info'

##### Default four element array
client_list = [client(),client(),client(),client()]
resize_height = 480+200
resize_weight = 640+600
name_space_height = 50
height = 480
weight = 640
refresh_img = False ##### refresh window
refresh_map = False ##### refresh map
click_to_cancel = False ##### cancel the sos signal
click_client = 0    ##### the client you click in window
x_bound = 620   ##### window x axis bound
y_bound = 340   ##### window y axis bound
#---------------------------------------------------------#
connection_num = np.zeros(4) 
inti_flag = -1
image = []
keep = []
middle_x = 1170 
middle_y = 700
init_time = 0
fireman_image_path = "../IMAGE/fireman.png"
environment_image_path = "../IMAGE/1f.png"
info_flag = -1
time_press = 0
info_image = np.zeros((800,800,3), np.uint8)

def emergency_cancel(event, x, y, flags, param):
    global click_to_cancel,click_client
    if event == cv2.EVENT_LBUTTONUP:  
        ##### Left Button Click
        #print("click:x= ",x,"  y= ",y)
        click_to_cancel = True
        if((x<=x_bound) and (y<= y_bound)):
            ##### client[0]
            click_client = 0
        elif((x>=x_bound) and (y<= y_bound)):
            ##### client[1]
            click_client = 1
        elif((x<=x_bound) and (y>= y_bound)):
            ##### client[2]
            click_client = 2
        elif((x>=x_bound) and (y>= y_bound)):
            ##### client[3]
            click_client = 3
        else:
            click_to_cancel = False           

def accept_wrapper(sock):
    global connection_num, inti_flag
    conn, addr = sock.accept()  # Should be ready to read
    print('accepted connection from', addr)
    
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)
    ##### create an client object an put into dictionary with it's address
    min_num = min(subplot_count)
    ##### create an white img with client name
    client_list[min_num]=client()
    client_dict[str(addr[1])] = min_num
    ##### number remove from list subplot_count
    subplot_count.remove(min_num)
    
    #--------------------------------------------------------------#
    i = 0                                                             
    while(i<4):
        if(connection_num[i] == 0):
            client_list[i].set_info(i,str(addr[0]))
            connection_num[i] = 1
            inti_flag = i
            break
        i = i + 1
    # add new connection
    # 創造一個新的Object給Device
#--------------------------------------------------------------------#
    
    print("Client: ")
    print("\tnum: ",client_list[i].id_num)
    print("\tip_addr: ",client_list[i].ip_addr)
    

def set_namespace_color(client_index,background_color,font_color):
    namespace_whiteimg = np.zeros((name_space_height,weight,3), np.uint8)
    namespace_whiteimg[:,:] = background_color
    name = client_list[client_index].get_name()
    cv2.putText(namespace_whiteimg, name, (200, 42), cv2.FONT_HERSHEY_SIMPLEX, 2, font_color, 3, cv2.LINE_AA)
    client_list[client_index].namespace_imgset(namespace_whiteimg)

def service_connection(key, mask):
    global connection_num, image, init_time

    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        global refresh_img,refresh_map
        recv_data = None
        client_host = client_dict[str(data.addr[1])]
        if(client_list[client_host].first_time_recv()):
            print("Getting Name...")
            recv_data = sock.recv(16)
            name = recv_data.decode()
            #name = (str)(client_list[client_host].get_num()) + "." + name
            client_list[client_host].set_name(name)
            ##### Default : white background black font
            set_namespace_color(client_host,(255,255,255),(0, 0, 0))   
            print("The Name is: ",name)
            
        else:
            if(client_list[client_host].package_size() < 0):
                try:
                    ##### recv the img size
                    recv_data = sock.recv(16)
                    recv_data_msg = recv_data.decode().strip()
                    if("SIZE" in recv_data_msg):
                        #print("image size msg")
                        client_list[client_host].package_set(int(recv_data_msg[4:len(recv_data_msg)]))
                    else:
                        #------------------------------------------------------------------#
                        for i in client_list:
                            if(i.ip_addr == str(data.addr[0])):
                                i.time_pass = time.time() - init_time
                                #print(i.time_pass)
                                if("HELP2" in recv_data_msg):
                                    #print("HELP2")
                                    helpConditionExec("HELP2",i.id_num)
                                    client_list[client_host].set_sos_flag(True)
                                    sock.send("I will save you".encode())
                                elif("HELP" in recv_data_msg):
                                    #print("HELP")
                                    helpConditionExec("HELP",i.id_num)
                                elif("num" in recv_data_msg):
                                    i.fire_num = recv_data_msg[4:len(recv_data_msg)]
                                    #print(i.fire_num)
                                else:
                                    print("id: ",i.id_num)
                                    print(recv_data_msg)
                                    drawNewSpot(recv_data_msg,i.id_num,img_fireman)                    
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
                client_list[client_host].img_combine(recv_data)
                client_list[client_host].package_decrease(len(recv_data))
                if(client_list[client_host].package_size() <= 0):
                    ##### img recv complete
                    client_list[client_host].img_decode()
                    client_list[client_host].package_set(-1)
                    refresh_img = True
                    ##### decide which background color to brush
                    brush_background_ornot = client_list[client_host].brush_background()
                    if(brush_background_ornot == 1):
                        ##### Red background white font
                        set_namespace_color(client_host,(0,0,255),(255, 255, 255))
                    elif (brush_background_ornot == 2):
                        ##### White background black font
                        set_namespace_color(client_host,(255,255,255),(0, 0, 0))
                #except Exception as e:
                #    print(e.args)

        if not recv_data:
            print('closing connection to', data.addr)
            #-------------------------------------------------------------------#
            print(str(data.addr[0]))
            print(client_list[0].ip_addr)
            for i in client_list:
                if(i.ip_addr == str(data.addr[0])):
                    connection_num[i.id_num] = 0
            refresh_map = True
            # Close Connection 的時候取消 Object
            #--------------------------------------------------------------------#
            client_list[client_dict[str(data.addr[1])]].set_visible(False)
            refresh_img = True
            subplot_count.append(client_dict[str(data.addr[1])])
            del client_dict[str(data.addr[1])]
            sel.unregister(sock)
            sock.close()

 #######    # running handling
def drawNewSpot(data,index,img_fireman):
    global client_list, keep, image, inti_flag, refresh_map

    image = keep.copy()
 
    left_spot_x = 5 + (middle_x-5)*(index%2)
    right_spot_x = middle_x + middle_x*(index%2)
    up_spot_y = 5 + (middle_y-5)*(index >= 2)
    down_spot_y = middle_y + (middle_y)*(index >= 2)
   
    client_list[index].color_set = (0,139,0)
    cv2.line(image,(left_spot_x,up_spot_y),(right_spot_x,up_spot_y),client_list[index].color_set,10,6)
    cv2.line(image,(left_spot_x,down_spot_y),(right_spot_x,down_spot_y),client_list[index].color_set,10,6)
    cv2.line(image,(left_spot_x,up_spot_y),(left_spot_x,down_spot_y),client_list[index].color_set,10,6)
    cv2.line(image,(right_spot_x,up_spot_y),(right_spot_x,down_spot_y),client_list[index].color_set,10,6)

    if("No Turn" in data):
         #print("index:",index)
        client_list[index].addNewPosition("No Turn",0)
    elif("Left" in data):
        client_list[index].addNewPosition("Left",0)
    elif("Right" in data):
        client_list[index].addNewPosition("Right",0)
    else:
        client_list[index].addNewPosition("No Turn",float(data))
    refresh_map = True
    #print('refresh')
    for i in range(4):
        image[client_list[i].position_y-25 : client_list[i].position_y + 25 , client_list[i].position_x-25 : client_list[i].position_x + 25] = img_fireman

def helpConditionExec(message,index):
    global image,refresh_map
    if("HELP2" in message):
        client_list[index].color_set = (0,0,255)
    elif("HELP" in message):
        client_list[index].color_set = (0,165,255)
    else:
        pass

    left_spot_x = 5 + (middle_x-5)*(index%2)
    right_spot_x = middle_x + middle_x*(index%2)
    up_spot_y = 5 + (middle_y-5)*(index >= 2)
    down_spot_y = middle_y + (middle_y)*(index >= 2)

    cv2.line(image,(left_spot_x,up_spot_y),(right_spot_x,up_spot_y),client_list[index].color_set,10,6)
    cv2.line(image,(left_spot_x,down_spot_y),(right_spot_x,down_spot_y),client_list[index].color_set,10,6)
    cv2.line(image,(left_spot_x,up_spot_y),(left_spot_x,down_spot_y),client_list[index].color_set,10,6)
    cv2.line(image,(right_spot_x,up_spot_y),(right_spot_x,down_spot_y),client_list[index].color_set,10,6)
    
    refresh_map = True

def addNewPoint(event,x,y,flags,param):
    global inti_flag
    global client_list

    if inti_flag != -1 and event == cv2.EVENT_LBUTTONDOWN:
        if client_list[inti_flag].position_x ==25 and client_list[inti_flag].position_y == 25:
            client_list[inti_flag].position_x = x
            client_list[inti_flag].position_y = y 
        else:
            temp_x = x
            temp_y = y
            if abs(temp_x-client_list[inti_flag].position_x) > abs(temp_y - client_list[inti_flag].position_y):
                if temp_x < client_list[inti_flag].position_x:
                    client_list[inti_flag].direction = 270
                else:
                    client_list[inti_flag].direction = 90
            else:
                if temp_y > client_list[inti_flag].position_y:
                    client_list[inti_flag].direction = 180
                else:
                    client_list[inti_flag].direction = 0
            print("inti:",inti_flag)
            print ("pos: ",(client_list[inti_flag].position_x,client_list[inti_flag].position_y))
            print ("dir: ",client_list[inti_flag].direction)
            inti_flag = -1


if __name__ == "__main__":
    img_fireman = []
    if(os.path.isfile(fireman_image_path)):
        pass
    else:
        print("There's no fireman image")
    print("Reading FireFighter Image...")
    while(len(img_fireman) == 0):
        img_fireman = cv2.imread(fireman_image_path)
    img_fireman = cv2.resize(img_fireman,(50,50))

    print("Reading Environment Map...")
    if(os.path.isfile(environment_image_path)):
        pass
    else:
        print("There's no environment image")
    while(len(image) == 0):
        image = cv2.imread(environment_image_path)

    print("Merge Map For Four FireFighters...")
    image = np.hstack((image,image))
    image = np.vstack((image,image))
    
    print("Setting Windows...")
    cv2.namedWindow(map_window_name,0)
    cv2.setWindowProperty(map_window_name,cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN )
    cv2.namedWindow(info_window_name,0)
    cv2.setWindowProperty(info_window_name,cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
    
    print("Drawing Security Line...")
    image = cv2.line(image,(5,5),(middle_x*2,5),(0,139,0),10,6)
    image = cv2.line(image,(5,middle_y),(middle_x*2,middle_y),(0,139,0),10,6)
    image = cv2.line(image,(5,middle_y*2),(middle_x*2,middle_y*2),(0,139,0),10,6)
    image = cv2.line(image,(5,5),(5,middle_y*2),(0,139,0),10,6)
    image = cv2.line(image,(middle_x,5),(middle_x,middle_y*2),(0,139,0),10,6)
    image = cv2.line(image,(middle_x*2,5),(middle_x*2,middle_y*2),(0,139,0),10,6)

    cv2.setMouseCallback(map_window_name,addNewPoint)
    keep = image.copy()

    ##### create a figure with subplot 2*5
    subplot_count = [0,1,2,3]
    cv2.namedWindow(img_window_name,cv2.WINDOW_NORMAL)
    cv2.setMouseCallback(img_window_name, emergency_cancel)
    cv2.moveWindow(img_window_name, 20,20)  # Move it to (40,30)
    ##### create a dictionary
    client_dict = {"client":1}

    try:
        
        sel = selectors.DefaultSelector()
        lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        lsock.bind((host, port))
        lsock.listen()
        print('listening on', (host, port))
        lsock.setblocking(False)
        sel.register(lsock, selectors.EVENT_READ, data=None)

        print("Waiting For Connection...")
        while True:
            #---------------------------------#
            if(keyboard.is_pressed('1') and time.time() - time_press > 1):
                time_press = time.time()
                info_flag = (info_flag != 0)*1 - 1
                print("pressed 1 , info_flag: ",info_flag)
            elif(keyboard.is_pressed('2') and time.time() - time_press > 1):
                time_press = time.time()
                info_flag = (info_flag != 1)*2 - 1
                print("pressed 2 , info_flag: ",info_flag)
            elif(keyboard.is_pressed('3') and time.time() - time_press > 1):
                time_press = time.time()
                info_flag = (info_flag != 2)*3 - 1
                print("pressed 3 , info _flag: ",info_flag)
            elif(keyboard.is_pressed('4') and time.time() - time_press > 1):
                time_press = time.time()
                info_flag = (info_flag != 3)*4 - 1
                print("pressed 4 , info_flag: ",info_flag)
            else:
                pass
            
            info_image = np.zeros((800,800,3),np.uint8)
            #---------------------------------#
            events = sel.select(timeout=None)
            for key, mask in events:
                if key.data is None:
                    accept_wrapper(key.fileobj)
                else:
                    service_connection(key, mask)
                    
                    if(refresh_img or refresh_map or info_flag >= 0):
                        if(refresh_img):
                            refresh_img = False
                            ##### concate and plot image
                            img_concate_Hori=np.concatenate((client_list[0].img_read(),client_list[1].img_read()),axis=1)
                            img_concate_Verti=np.concatenate((client_list[2].img_read(),client_list[3].img_read()),axis=1)
                            img_toshow = np.concatenate((img_concate_Hori,img_concate_Verti),axis=0)
                            img_toshow = cv2.resize(img_toshow,(resize_weight,resize_height),interpolation=cv2.INTER_CUBIC)
                            cv2.imshow(img_window_name,img_toshow)
                            #cv2.waitKey(1)
                        if(refresh_map):
                            #print("refresh map")
                            refresh_map = False
                            #-------------------------------------------------------------#
                            # to show image
                            cv2.imshow(map_window_name,image)
                            '''
                            if cv2.waitKey(1) & 0xFF == ord('q'):
                                break
                            '''
                            # Show 我們的圖
                            #-----------------------------------------------------------------#
                        ###
                        if(info_flag >= 0):
                            cv2.putText(info_image,"Name: "+str(client_list[info_flag].name), (10, 40), cv2.FONT_HERSHEY_SIMPLEX,1, (0, 255, 255), 1, cv2.LINE_AA)
                            cv2.putText(info_image,"Number: "+str(client_list[info_flag].fire_num), (10, 60), cv2.FONT_HERSHEY_SIMPLEX,1, (0, 255, 255), 1, cv2.LINE_AA)
                            cv2.putText(info_image,"Time Pass: "+str(client_list[info_flag].time_pass), (10, 80), cv2.FONT_HERSHEY_SIMPLEX,1, (0, 255, 255), 1, cv2.LINE_AA)
                        cv2.imshow(info_window_name,info_image)                        
                        ###
 
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break
                    if(click_to_cancel):
                        set_namespace_color(click_client,(255,255,255),(0, 0, 0))
                        client_list[click_client].set_sos_flag(False)
                        click_to_cancel = False
            
                    
    finally:
        lsock.close()
        cv2.destroyAllWindows()
        print("close socket")
