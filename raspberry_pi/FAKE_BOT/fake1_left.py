import socket
import time
HOST = '192.168.68.100'
PORT = 8888

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST,PORT))

count = 0

def print_no_move():
    global s
    s.send(("No Turn").ljust(16))
  #  d = s.recv(1024)
    s.send(("0.0").ljust(16))
  #  d = s.recv(1024)
    time.sleep(1)
def walk():
	global s
	s.send(("No Turn").ljust(16))
#	d = s.recv(1024)
	s.send(("1.5").ljust(16))
#	d = s.recv(1024)
	time.sleep(1)
	s.send(("No Turn").ljust(16))
#	d = s.recv(1024)
	s.send(("1.3").ljust(16))
#	d = s.recv(1024)
	time.sleep(1)
	s.send(("No Turn").ljust(16))
#	d = s.recv(1024)
	s.send(("1.4").ljust(16))
#	d = s.recv(1024)
	time.sleep(1)
	s.send(("No Turn").ljust(16))
#	d = s.recv(1024)
	s.send(("1.2").ljust(16))
#	d = s.recv(1024)
	time.sleep(1)
	s.send(("No Turn").ljust(16))
#	d = s.recv(1024)
	s.send(("1.2").ljust(16))
#	d = s.recv(1024)
	time.sleep(1)
	s.send(("Left").ljust(16))
#	d = s.recv(1024)
	s.send(("0.0").ljust(16))
#	d = s.recv(1024)
	time.sleep(1)

	s.send(("No Turn").ljust(16))
	#d = s.recv(1024)
	s.send(("1.5").ljust(16))
	#d = s.recv(1024)
	time.sleep(1)
	s.send(("No Turn").ljust(16))
#	d = s.recv(1024)
	s.send(("1.5").ljust(16))
#	d = s.recv(1024)
	time.sleep(1)
	s.send(("No Turn").ljust(16))
#	d = s.recv(1024)
	s.send(("1.5").ljust(16))
#	d = s.recv(1024)
	time.sleep(1)
	s.send(("No Turn").ljust(16))
#	d = s.recv(1024)
	s.send(("1.5").ljust(16))
#	d = s.recv(1024)
	time.sleep(1)
	s.send(("No Turn").ljust(16))
#	d = s.recv(1024)
	s.send(("1.5").ljust(16))
#	d = s.recv(1024)
	time.sleep(1)
	s.send(("No Turn").ljust(16))
#	d = s.recv(1024)
	s.send(("1.5").ljust(16))
#	d = s.recv(1024)
	time.sleep(1)
	s.send(("No Turn").ljust(16))
#	d = s.recv(1024)
	s.send(("1.5").ljust(16))
#	d = s.recv(1024)
	time.sleep(1)
	s.send(("No Turn").ljust(16))
#	d = s.recv(1024)
	s.send(("1.5").ljust(16))
#	d = s.recv(1024)
	time.sleep(1)
	s.send(("No Turn").ljust(16))
#	d = s.recv(1024)
	s.send(("1.5").ljust(16))
#	d = s.recv(1024)
	time.sleep(1)

	s.send(("Left").ljust(16))
#	d = s.recv(1024)
	s.send(("0.0").ljust(16))
#	d = s.recv(1024)
	s.send(("Left").ljust(16))
#	d = s.recv(1024)
	s.send(("0.0").ljust(16))
#	d = s.recv(1024)
	time.sleep(1)

	s.send(("No Turn").ljust(16))
#	d = s.recv(1024)
	s.send(("1.5").ljust(16))
#	d = s.recv(1024)
	time.sleep(1)
	s.send(("No Turn").ljust(16))
#	d = s.recv(1024)
	s.send(("1.5").ljust(16))
#	d = s.recv(1024)
	time.sleep(1)
	s.send(("No Turn").ljust(16))
#	d = s.recv(1024)
	s.send(("1.5").ljust(16))
#	d = s.recv(1024)
	time.sleep(1)
	s.send(("No Turn").ljust(16))
#	d = s.recv(1024)
	s.send(("1.5").ljust(16))
#	d = s.recv(1024)
	time.sleep(1)
	s.send(("No Turn").ljust(16))
#	d = s.recv(1024)
	s.send(("1.5").ljust(16))
#	d = s.recv(1024)
	time.sleep(1)
	s.send(("No Turn").ljust(16))
#	d = s.recv(1024)
	s.send(("1.5").ljust(16))
#	d = s.recv(1024)
	time.sleep(1)
	s.send(("No Turn").ljust(16))
#	d = s.recv(1024)
	s.send(("1.5").ljust(16))
#	d = s.recv(1024)
	time.sleep(1)
	help1()
	help1()
	help1()
	help1()
	help2()
	help2()
	help2()
	help2()
	s.send(("No Turn").ljust(16))
#	d = s.recv(1024)
	s.send(("1.5").ljust(16))
#	d = s.recv(1024)
	time.sleep(1)
	s.send(("No Turn").ljust(16))
#	d = s.recv(1024)
	s.send(("1.5").ljust(16))
#	d = s.recv(1024)
	time.sleep(1)

	s.send(("Right").ljust(16))
#	d = s.recv(1024)
	s.send(("0.0").ljust(16))
	time.sleep(1)
#	d = s.recv(1024)
	s.send(("No Turn").ljust(16))
#	d = s.recv(1024)
	s.send(("1.5").ljust(16))
#	d = s.recv(1024)
	time.sleep(1)
	s.send(("No Turn").ljust(16))
#	d = s.recv(1024)
	s.send(("1.3").ljust(16))
#	d = s.recv(1024)
	time.sleep(1)
	s.send(("No Turn").ljust(16))
#	d = s.recv(1024)
	s.send(("1.4").ljust(16))
#	d = s.recv(1024)
	time.sleep(1)
	s.send(("No Turn").ljust(16))
#	d = s.recv(1024)
	s.send(("1.2").ljust(16))
#	d = s.recv(1024)
	time.sleep(1)
	s.send(("No Turn").ljust(16))
#	d = s.recv(1024)
	s.send(("1.2").ljust(16))
#	d = s.recv(1024)
	time.sleep(1)
	s.send(("Left").ljust(16))
#	d = s.recv(1024)
	s.send(("0.0").ljust(16))
#	d = s.recv(1024)
	time.sleep(1)
	s.send(("Left").ljust(16))
#	d = s.recv(1024)
	s.send(("0.0").ljust(16))
#	d = s.recv(1024)
	time.sleep(1)
	
def help1():
	s.send(("HELP").ljust(16))
	print("HELP")
#	d = s.recv(1024)
#	print(d)
	time.sleep(1)
def help2():
	s.send(("HELP2").ljust(16))
	print("HELP2")
#	d = s.recv(1024)
#	print(d)
	time.sleep(1)

try:
	while True:
		if count == 0:
			s.send(("aaaname").ljust(16));
			print("aaaname")
		#	d = s.recv(1024)
		while count < 5:
			print_no_move()
			count += 1
			print("NO")
		#s.send(("num_0426").ljust(16))
		#d = s.recv(1024)
		#s.send(("name_Winnie The Pooh").ljust(16))
		#d = s.recv(1024)
		#time.sleep(1)
		while count >= 5:
			walk()
			count += 5
			print("walk")
finally:
	s.close()
	print('close')
