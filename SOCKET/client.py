import socket

HOST = '192.168.68.97'
PORT = 7777

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST,PORT))
try:
    while True:
        cmd = raw_input("Please input msg:")
        s.send(cmd)
        data = s.recv(1024)
        print(data)
finally:
    s.close()
    print('close')
