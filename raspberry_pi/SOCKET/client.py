import socket

<<<<<<< HEAD:SOCKET/client.py
HOST = '192.168.68.97'
PORT = 8888
=======
HOST = '192.168.68.98'
PORT = 7777
>>>>>>> ad284bd5cb854c359fbe953ae26e5617e3726996:raspberry_pi/SOCKET/client.py

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST,PORT))

try:
    while True:
<<<<<<< HEAD:SOCKET/client.py
        cmd = input("Please input msg:")
=======
        i = 0
        cmd = "No Turn"
>>>>>>> ad284bd5cb854c359fbe953ae26e5617e3726996:raspberry_pi/SOCKET/client.py
        s.send(cmd)
        data = s.recv(1024)
        print(data)
        while i < 100000:
            i += 1
finally:
    s.close()
    print('close')
