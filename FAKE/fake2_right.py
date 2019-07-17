import socket
import time
HOST = '192.168.68.100'
PORT = 8888

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST,PORT))

count = 0

def print_no_move():
    global s
    s.send("No Turn")
    d = s.recv(1024)
    s.send("0.0")
    d = s.recv(1024)
    time.sleep(1)
def walk():
    global s
    s.send("No Turn")
    d = s.recv(1024)
    s.send("1.2")
    d = s.recv(1024)
    time.sleep(1)
    s.send("No Turn")
    d = s.recv(1024)
    s.send("1.2")
    d = s.recv(1024)
    time.sleep(1)
    s.send("No Turn")
    d = s.recv(1024)
    s.send("1.2")
    d = s.recv(1024)
    time.sleep(1)
    s.send("No Turn")
    d = s.recv(1024)
    s.send("1.2")
    d = s.recv(1024)
    time.sleep(1)
    s.send("No Turn")
    d = s.recv(1024)
    s.send("1.2")
    d = s.recv(1024)
    time.sleep(1)
    s.send("Right")
    d = s.recv(1024)
    s.send("0.0")
    d = s.recv(1024)
    time.sleep(1)
def help1():
    s.send("HELP")
    d = s.recv(1024)
    time.sleep(1)
def help2():
    s.send("HELP2")
    d = s.recv(1024)
    time.sleep(1)

try:
    while True:
        while count < 5:
            print_no_move()
            count += 1
            print("NO")
        while count >= 5 and count < 25:
            walk()
            count += 5
            print("walk")
        while count >= 25 and count < 30:
            help1()
            count += 1
            print("help1")
        while count >= 30:
            help2()
            count += 1
            print("help2")
            if count == 35:
                count = 5
        print(count)
finally:
	s.close()
	print('close')
