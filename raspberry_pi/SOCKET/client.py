import socket

HOST = '192.168.68.98'
PORT = 7777

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST,PORT))

try:
    while True:
        i = 0
        cmd = "No Turn"
        s.send(cmd)
        data = s.recv(1024)
        print(data)
        while i < 100000:
            i += 1
finally:
    s.close()
    print('close')
