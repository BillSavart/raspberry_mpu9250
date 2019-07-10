import cv2
import numpy as np
import time
import socket
import selectors
import types
from structure_connect import StructureConnection
import multiprocessing as mp

inti_flag = -1
connection_arr = list()
connection_num = np.zeros(9)
host = '192.168.68.97'
port = 8888

keep = np.array([0,0,3])
middle_x = 1170 
middle_y = 720

def localbot():
    bot1_arr = [[0,1],[0,2],[0,3],[0,4]]
    bot2_arr = [[3,4],[4,6],[5,7],[6,8]]
    bot3_arr = [[8,0],[6,1],[7,1],[9,0]]

    bot1_p = 0
    bot2_p = 0
    bot3_p = 0

    while True:
        bot1_x.value = bot1_arr[bot1_p][0]
        bot1_y.value = bot1_arr[bot1_p][1]
        bot2_x.value = bot2_arr[bot2_p][0]
        bot2_y.value = bot2_arr[bot2_p][1]
        bot3_x.value = bot3_arr[bot3_p][0]
        bot3_y.value = bot3_arr[bot3_p][1] 
        bot1_p = bot1_p + 1
        if(bot1_p >= len(bot1_arr)):
            bot1_p = bot1_p % len(bot1_arr)
        bot2_p = bot2_p + 1
        if(bot2_p >= len(bot2_arr)):      
            bot2_p = bot2_p % len(bot2_arr)
        bot3_p = bot3_p + 1       
        if(bot3_p >= len(bot3_arr)):      
            bot3_p = bot3_p % len(bot3_arr)
        time.sleep(1)

def accept_wrapper(sock,sel):
    global connection_arr
    global connection_num
    global inti_flag

    conn, addr = sock.accept()  # Should be ready to read
    print('accepted connection from', addr)
#--------------------------------------------------------------------#
    i = 0
    while(i<10):
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

def service_connection(key, mask,sel,image,img_fireman):
    global connection_arr
    global connection_num
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
                if(i.ip_addr == str(data.addr[0])):
                    connection_num[i] = 0

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
                    if(data.outb.decode() == "HELP"):
                        helpConditionExec("HELP",i.id_num,image)
                    elif(data.outb.decode() == "HELP2"):
                        helpConditionExec("HELP2",i.id_num,image)
                    else:
                        drawNewSpot(image,img_fireman,data.outb.decode(),i.id_num)                    
                    break
            # Device 傳輸資料時, call 對應function
#--------------------------------------------------------------------#
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]
    
 #######    # running handling
def drawNewSpot(image,img_fireman,data,index):
    global connection_arr
    global keep 

    print(type(keep))
    print(type(image))

    image = keep
#    cv2.putText(image,str(connection_arr[index].id_num+1),(connection_arr[index].position_x,connection_arr[index].position_y),cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),3)
    if(data != "HELP"):
        cv2.line(image,(5,5),(middle_x,5),(0,139,0),10,6)
        cv2.line(image,(5,middle_y),(middle_x,middle_y),(0,139,0),10,6)
        cv2.line(image,(5,5),(5,middle_y),(0,139,0),10,6)
        cv2.line(image,(middle_x,5),(middle_x,middle_y),(0,139,0),10,6)
        if(data == "No Turn" or data == "Left" or data == "Right"):
            connection_arr[index].color_set = (0,139,0)
            connection_arr[index].addNewPosition(data,0,image)
        else:
            connection_arr[index].color_set = (0,139,0)
            connection_arr[index].addNewPosition("No Turn",float(data),image)
    
    image[connection_arr[index].position_x-10 : connection_arr[index].position_x + 10 , connection_arr[index].position_y-10 : connection_arr[index].position_y + 10] = 0
    
 #   cv2.putText(image,str(connection_arr[index].id_num+1),(connection_arr[index].position_x,connection_arr[index].position_y),cv2.FONT_HERSHEY_PLAIN,2,connection_arr[index].color_set,3)

def helpConditionExec(message,num,image):
    if(message == "HELP"):
        connection_arr[num].color_set = (0,165,255)
        cv2.line(image,(5,5),(middle_x,5),(0,165,255),10,6)
        cv2.line(image,(5,middle_y),(middle_x,middle_y),(0,165,255),10,6)
        cv2.line(image,(5,5),(5,middle_y),(0,165,255),10,6)
        cv2.line(image,(middle_x,5),(middle_x,middle_y),(0,165,255),10,6)
    elif (message == "HELP2"):
        connection_arr[num].color_set = (0,0,255)
        cv2.line(image,(5,5),(middle_x,5),(0,0,255),10,6)
        cv2.line(image,(5,middle_y),(middle_x,middle_y),(0,0,255),10,6)
        cv2.line(image,(5,5),(5,middle_y),(0,0,255),10,6)
        cv2.line(image,(middle_x,5),(middle_x,middle_y),(0,0,255),10,6)

    else:
       pass

def addNewPoint(event,x,y,flags,param):
    global inti_flag
    global connection_arr

    if inti_flag != -1 and event == cv2.EVENT_LBUTTONDOWN:
        if connection_arr[inti_flag].position_x == 0 and connection_arr[inti_flag].position_y == 0:
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

def drawbot(image):
    global bot1_old_x
    global bot1_old_y
    global bot2_old_x
    global bot2_old_y
    global bot3_old_x
    global bot3_old_y

#    cv2.putText(image,"2",(bot1_old_x.value,bot1_old_y.value),cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),3)
#    cv2.putText(image,"2",(bot1_x.value,bot1_y.value),cv2.FONT_HERSHEY_PLAIN,2,(0,139,0),3)
#    cv2.putText(image,"3",(bot2_old_x.value,bot2_old_y.value),cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),3)
#    cv2.putText(image,"3",(bot2_x.value,bot2_y.value),cv2.FONT_HERSHEY_PLAIN,2,(0,139,0),3)
#    cv2.putText(image,"4",(bot3_old_x.value,bot3_old_y.value),cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),3)
#    cv2.putText(image,"4",(bot3_x.value,bot3_y.value),cv2.FONT_HERSHEY_PLAIN,2,(0,139,0),3)
    bot1_old_x = bot1_x.value
    bot1_old_y = bot1_y.value    
    bot2_old_x = bot2_x.value
    bot2_old_y = bot2_y.value
    bot3_old_x = bot3_x.value
    bot3_old_y = bot3_y.value

def main():
    global connection_arr
    global bot1_old_x
    global bot1_old_y
    global bot2_old_x
    global bot2_old_y
    global bot3_old_x
    global bot3_old_y

    i = 0
    while(i<10):
        connection_arr.append(StructureConnection(0,"0"))
        i = i + 1
    
    img_fireman = cv2.imread("../IMAGE/fireman.png")
    img_fireman = cv2.resize(img_fireman,(20,20))

    image = cv2.imread("../IMAGE/5f.png")
    image1 = cv2.imread("../IMAGE/5f.png")
    image2 = cv2.imread("../IMAGE/5f.png")
    image3 = cv2.imread("../IMAGE/5f.png")
    image = np.hstack((image,image1))
    image1 = np.hstack((image2,image3))
    image = np.vstack((image,image1))
    keep = image
    cv2.namedWindow("Image",0)
    cv2.setWindowProperty("Image",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN )
    cv2.setMouseCallback("Image",addNewPoint)
    
    image = cv2.line(image,(5,5),(middle_x*2,5),(0,139,0),10,6)
    image = cv2.line(image,(5,middle_y),(middle_x*2,middle_y),(0,139,0),10,6)
    image = cv2.line(image,(5,middle_y*2),(middle_x*2,middle_y*2),(0,139,0),10,6)
    image = cv2.line(image,(5,5),(5,middle_y*2),(0,139,0),10,6)
    image = cv2.line(image,(middle_x,5),(middle_x,middle_y*2),(0,139,0),10,6)
    image = cv2.line(image,(middle_x*2,5),(middle_x*2,middle_y*2),(0,139,0),10,6)

    cv2.imshow("Image",image)
    
 #   bot = mp.Process(target = localbot)
 #   bot.start()

    try:
        sel = selectors.DefaultSelector()

        lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        lsock.bind((host, port))
        lsock.listen()
        print('listening on', (host, port))
        lsock.setblocking(False)
        sel.register(lsock, selectors.EVENT_READ, data=None)
        while True:
            events = sel.select(timeout=None)########shutttttttt down
            #drawbot(image)
            for key, mask in events:      
                if key.data is None:
                    accept_wrapper(key.fileobj,sel)
                else:
                    service_connection(key, mask,sel,image,img_fireman)    
#-------------------------------------------------------------#
# to show image
            cv2.imshow("Image",image)
            if cv2.waitKey(500) & 0xFF == ord('q'):
                break
            # Show 我們的圖
#-----------------------------------------------------------------#
    finally:
        lsock.close()
#        bot.join()
        print("close socket")


if __name__ == "__main__" :
    bot1_x = mp.Value("i",0)    
    bot1_y = mp.Value("i",0)
    bot2_x = mp.Value("i",0)
    bot2_y = mp.Value("i",0)
    bot3_x = mp.Value("i",0)
    bot3_y = mp.Value("i",0)
    bot1_old_x = bot1_x.value
    bot1_old_y = bot1_y.value
    bot2_old_x = bot2_x.value
    bot2_old_y = bot2_y.value
    bot3_old_x = bot3_x.value
    bot3_old_y = bot3_y.value
    main()
