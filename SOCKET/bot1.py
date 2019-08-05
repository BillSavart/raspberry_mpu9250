import socket

HOST = '192.168.68.100'
PORT = 8888

array = ["0.1","0.1","0.1","0.1"]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST,PORT))
try:
    while True:
        pass
#        for i in array:
#            s.send(str(i))
#            data = s.recv(1024)
#            print(data)
finally:
    s.close()
    print('close')
