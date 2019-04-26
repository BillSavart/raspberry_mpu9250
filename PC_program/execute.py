import cv2
import numpy as np
import time
import socket
import selectors
import types
from structure_connect import StructureConnection

inti_flag = -1
connection_arr = list()
connection_num = np.zeros(9)
host = '192.168.68.98'
port = 7777
 
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
#--------------------------------------------------------------------#
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)

def service_connection(key, mask,sel,image):
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
#            if(str(data.addr[0]) == connection_arr[0].ip_addr):
#                print("Yes")
 #           for i in connection_arr:
 #               if(i.ip_addr == str(data.addr[0])):
 #                   print("Yes")
 #                   break
#--------------------------------------------------------------------#
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print('echoing', repr(data.outb), 'to', data.addr)
#------------------------------------------------------------------#
            for i in connection_arr:
                if(i.ip_addr == str(data.addr[0])):
                    drawNewSpot(image,data.outb.decode(),i.id_num)
                    break
#--------------------------------------------------------------------#
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]
    
 #######    # running handling
def drawNewSpot(image,data,index):
    global connection_arr

    cv2.putText(image,str(connection_arr[index].id_num+1),(connection_arr[index].position_x,connection_arr[index].position_y),cv2.FONT_HERSHEY_PLAIN,1,(255,255,255),2)
    connection_arr[index].addNewPosition(data,0.1,image)
    cv2.putText(image,str(connection_arr[index].id_num+1),(connection_arr[index].position_x,connection_arr[index].position_y),cv2.FONT_HERSHEY_PLAIN,1,connection_arr[index].color_set,2)


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

def main():
    global connection_arr

    i = 0
    while(i<10):
        connection_arr.append(StructureConnection(0,"0"))
        i = i + 1

    image = cv2.imread("../IMAGE/image_draw.JPG")
    cv2.namedWindow("Image")
    cv2.setMouseCallback("Image",addNewPoint)
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
            events = sel.select(timeout=None)########shutttttttt down
            for key, mask in events:      
                if key.data is None:
                    accept_wrapper(key.fileobj,sel)
                else:
                    service_connection(key, mask,sel,image)    
#-------------------------------------------------------------#
# to show image 
            cv2.imshow("Image",image)
            if cv2.waitKey(500) & 0xFF == ord('q'):
                break
#-----------------------------------------------------------------#
    finally:
        lsock.close()
        print("close socket")


if __name__ == "__main__" :
    main()
