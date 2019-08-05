import cv2
import numpy as np
import time
import socket
import selectors
import types
from structure_connect import StructureConnection
import keyboard
import os

inti_flag = -1
connection_arr = list()
connection_num = np.zeros(4)
host = '192.168.68.100'
port = 8888

image = []
keep = []
middle_x = 1170 
middle_y = 700
init_time = 0

def accept_wrapper(sock,sel):
    global connection_arr
    global connection_num
    global inti_flag

    conn, addr = sock.accept()  # Should be ready to read
    print('accepted connection from', addr)
#--------------------------------------------------------------------#
    i = 0
    while(i<4):
        if(connection_num[i] == 0):
            connection_arr[i] = StructureConnection(i,str(addr[0]))
            connection_num[i] = 1
            inti_flag = i
            break
        i = i + 1
    # add new connection
    # 創造一個新的Object給Device
#--------------------------------------------------------------------#
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)

def service_connection(key, mask,sel,img_fireman):
    global connection_arr
    global connection_num
    global image
    global init_time

    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            data.outb += recv_data
        else:
            print('closing connection to', data.addr)
#-------------------------------------------------------------------#
            print(str(data.addr[0]))
            print(connection_arr[0].ip_addr)
            for i in connection_arr:
                print(i.id_num)
                if(i.ip_addr == str(data.addr[0])):
                    connection_num[i.id_num] = 0

            # Close Connection 的時候取消 Object
#--------------------------------------------------------------------#
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print('echoing', repr(data.outb), 'to', data.addr)
#------------------------------------------------------------------#
            for i in connection_arr:
                if(i.ip_addr == str(data.addr[0])):
                    i.time_pass = time.time() - init_time
                    print(i.time_pass)
                    if(data.outb.decode() == "HELP"):
                        helpConditionExec("HELP",i.id_num)
                    elif(data.outb.decode() == "HELP2"):
                        helpConditionExec("HELP2",i.id_num)
                    elif(data.outb.decode()[0:4] == "num_"):
                        i.fire_num = data.outb.decode()[4:len(data.outb.decode())]
                        print(i.fire_num)
                    elif(data.outb.decode()[0:5] == "name_"):
                        i.fire_name = data.outb.decode()[5:len(data.outb.decode())]
                        print(i.fire_name)
                    else:
                        drawNewSpot(data.outb.decode(),i.id_num,img_fireman)                    
                    break
            # Device 傳輸資料時, call 對應function
#--------------------------------------------------------------------#
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]
    
 #######    # running handling
def drawNewSpot(data,index,img_fireman):
    global connection_arr
    global keep 
    global image
    global inti_flag    

    image = keep.copy()
    if(data != "HELP" or data != "HELP2"):
        if(index == 0):
            cv2.line(image,(5,5),(middle_x,5),(0,139,0),10,6)
            cv2.line(image,(5,middle_y),(middle_x,middle_y),(0,139,0),10,6)
            cv2.line(image,(5,5),(5,middle_y),(0,139,0),10,6)
            cv2.line(image,(middle_x,5),(middle_x,middle_y),(0,139,0),10,6)
        elif (index == 1):
            cv2.line(image,(middle_x,5),(middle_x*2,5),(0,139,0),10,6)
            cv2.line(image,(middle_x,middle_y),(middle_x*2,middle_y),(0,139,0),10,6)
            cv2.line(image,(middle_x*2,5),(middle_x*2,middle_y),(0,139,0),10,6)
            cv2.line(image,(middle_x,5),(middle_x,middle_y),(0,139,0),10,6)
        elif(index == 2):
            cv2.line(image,(5,middle_y),(5,middle_y*2),(0,139,0),10,6)
            cv2.line(image,(middle_x,middle_y),(middle_x,middle_y*2),(0,139,0),10,6)
            cv2.line(image,(5,middle_y),(middle_x,middle_y),(0,139,0),10,6)
            cv2.line(image,(5,middle_y*2),(middle_x,middle_y*2),(0,139,0),10,6)
        elif(index == 3):
            cv2.line(image,(middle_x,middle_y),(middle_x*2,middle_y),(0,139,0),10,6)
            cv2.line(image,(middle_x,middle_y*2),(middle_x*2,middle_y*2),(0,139,0),10,6)
            cv2.line(image,(middle_x,middle_y),(middle_x,middle_y*2),(0,139,0),10,6)
            cv2.line(image,(middle_x*2,middle_y),(middle_x*2,middle_y*2),(0,139,0),10,6)
        else:
            pass
        if(data == "No Turn" or data == "Left" or data == "Right"):
            print("index:",index)
            connection_arr[index].color_set = (0,139,0)
            connection_arr[index].addNewPosition(data,0)
        else:
            connection_arr[index].color_set = (0,139,0)
            connection_arr[index].addNewPosition("No Turn",float(data))
    for i in range(4):
        image[connection_arr[i].position_y-25 : connection_arr[i].position_y + 25 , connection_arr[i].position_x-25 : connection_arr[i].position_x + 25] = img_fireman

def helpConditionExec(message,num):
    global image
    if(message == "HELP"):
        connection_arr[num].color_set = (0,165,255)
        if(num == 0):
            cv2.line(image,(5,5),(middle_x,5),(0,165,255),10,6)
            cv2.line(image,(5,middle_y),(middle_x,middle_y),(0,165,255),10,6)
            cv2.line(image,(5,5),(5,middle_y),(0,165,255),10,6)
            cv2.line(image,(middle_x,5),(middle_x,middle_y),(0,165,255),10,6)
        elif (num == 1):
            cv2.line(image,(middle_x,5),(middle_x*2,5),(0,165,255),10,6) 
            cv2.line(image,(middle_x,middle_y),(middle_x*2,middle_y),(0,165,255),10,6)
            cv2.line(image,(middle_x*2,5),(middle_x*2,middle_y),(0,165,255),10,6)
            cv2.line(image,(middle_x,5),(middle_x,middle_y),(0,165,255),10,6)
        elif(num == 2):                                    
            cv2.line(image,(5,middle_y),(5,middle_y*2),(0,165,255),10,6) 
            cv2.line(image,(middle_x,middle_y),(middle_x,middle_y*2),(0,165,255),10,6)
            cv2.line(image,(5,middle_y),(middle_x,middle_y),(0,165,255),10,6)
            cv2.line(image,(5,middle_y*2),(middle_x,middle_y*2),(0,165,255),10,6)
        elif(num == 3): 
            cv2.line(image,(middle_x,middle_y),(middle_x*2,middle_y),(0,165,255),10,6)
            cv2.line(image,(middle_x,middle_y*2),(middle_x*2,middle_y*2),(0,165,255),10,6)
            cv2.line(image,(middle_x,middle_y),(middle_x,middle_y*2),(0,165,255),10,6)
            cv2.line(image,(middle_x*2,middle_y),(middle_x*2,middle_y*2),(0,165,255),10,6)
        else:    
            pass 
    elif (message == "HELP2"):
        connection_arr[num].color_set = (0,0,255)
        if(num == 0):
            cv2.line(image,(5,5),(middle_x,5),(0,0,255),10,6)
            cv2.line(image,(5,middle_y),(middle_x,middle_y),(0,0,255),10,6)
            cv2.line(image,(5,5),(5,middle_y),(0,0,255),10,6)
            cv2.line(image,(middle_x,5),(middle_x,middle_y),(0,0,255),10,6)
        elif (num == 1):
            cv2.line(image,(middle_x,5),(middle_x*2,5),(0,0,255),10,6) 
            cv2.line(image,(middle_x,middle_y),(middle_x*2,middle_y),(0,0,255),10,6)
            cv2.line(image,(middle_x*2,5),(middle_x*2,middle_y),(0,0,255),10,6)
            cv2.line(image,(middle_x,5),(middle_x,middle_y),(0,0,255),10,6)
        elif(num == 2):                                    
            cv2.line(image,(5,middle_y),(5,middle_y*2),(0,0,255),10,6) 
            cv2.line(image,(middle_x,middle_y),(middle_x,middle_y*2),(0,0,255),10,6)
            cv2.line(image,(5,middle_y),(middle_x,middle_y),(0,0,255),10,6)
            cv2.line(image,(5,middle_y*2),(middle_x,middle_y*2),(0,0,255),10,6)
        elif(num == 3): 
            cv2.line(image,(middle_x,middle_y),(middle_x*2,middle_y),(0,0,255),10,6)
            cv2.line(image,(middle_x,middle_y*2),(middle_x*2,middle_y*2),(0,0,255),10,6)
            cv2.line(image,(middle_x,middle_y),(middle_x,middle_y*2),(0,0,255),10,6)
            cv2.line(image,(middle_x*2,middle_y),(middle_x*2,middle_y*2),(0,0,255),10,6)
        else:    
            pass 
    else:
       pass

def addNewPoint(event,x,y,flags,param):
    global inti_flag
    global connection_arr

    if inti_flag != -1 and event == cv2.EVENT_LBUTTONDOWN:
        if connection_arr[inti_flag].position_x ==25 and connection_arr[inti_flag].position_y == 25:
            connection_arr[inti_flag].position_x = x
            connection_arr[inti_flag].position_y = y 
        else:
            temp_x = x
            temp_y = y
            if abs(temp_x-connection_arr[inti_flag].position_x) > abs(temp_y - connection_arr[inti_flag].position_y):
                if temp_x < connection_arr[inti_flag].position_x:
                    connection_arr[inti_flag].direction = 270
                else:
                    connection_arr[inti_flag].direction = 90
            else:
                if temp_y > connection_arr[inti_flag].position_y:
                    connection_arr[inti_flag].direction = 180
                else:
                    connection_arr[inti_flag].direction = 0
            print ("dir: ",connection_arr[inti_flag].direction)
            inti_flag = -1

def show_info():
    os.system("sudo python3 show_info.py")    

def main():
    global image
    global connection_arr
    global keep
    global init_time

    init_time = time.time()

    i = 0
    while(i<10):
        connection_arr.append(StructureConnection(0,"0"))
        i = i + 1
    
    img_fireman = cv2.imread("../IMAGE/fireman.png")
    img_fireman = cv2.resize(img_fireman,(50,50))

    image = cv2.imread("../IMAGE/5f.png")
    image1 = cv2.imread("../IMAGE/5f.png")
    image2 = cv2.imread("../IMAGE/5f.png")
    image3 = cv2.imread("../IMAGE/5f.png")
    image = np.hstack((image,image1))
    image1 = np.hstack((image2,image3))
    image = np.vstack((image,image1))
    
    cv2.namedWindow("Image",0)
    cv2.setWindowProperty("Image",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN )
    
    image = cv2.line(image,(5,5),(middle_x*2,5),(0,139,0),10,6)
    image = cv2.line(image,(5,middle_y),(middle_x*2,middle_y),(0,139,0),10,6)
    image = cv2.line(image,(5,middle_y*2),(middle_x*2,middle_y*2),(0,139,0),10,6)
    image = cv2.line(image,(5,5),(5,middle_y*2),(0,139,0),10,6)
    image = cv2.line(image,(middle_x,5),(middle_x,middle_y*2),(0,139,0),10,6)
    image = cv2.line(image,(middle_x*2,5),(middle_x*2,middle_y*2),(0,139,0),10,6)

    cv2.setMouseCallback("Image",addNewPoint)
    keep = image.copy()

    cv2.imshow("Image",image)
    
    try:
        sel = selectors.DefaultSelector()

        lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        lsock.bind((host, port))
        lsock.listen()
        print('listening on', (host, port))
        lsock.setblocking(False)
        sel.register(lsock, selectors.EVENT_READ, data=None)
        while True:
            if(keyboard.is_pressed('i')):
                show_info()
            events = sel.select(timeout=None)########shutttttttt down
            for key, mask in events:      
                if key.data is None:
                    accept_wrapper(key.fileobj,sel)
                else:
                    service_connection(key, mask,sel,img_fireman)    
#-------------------------------------------------------------#
# to show image
            cv2.imshow("Image",image)
            if cv2.waitKey(500) & 0xFF == ord('q'):
                break
            # Show 我們的圖
#-----------------------------------------------------------------#
    finally:
        lsock.close()
        print("close socket")


if __name__ == "__main__" :
    main()
