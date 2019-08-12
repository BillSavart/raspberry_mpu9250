import socket
import time
HOST = '192.168.68.100'
PORT = 6667

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST,PORT))

def move1():
	print("enter function_1")
	count = 0
	s.send((("0.0").encode()).ljust(16))
	print("0.0")
	s.send((("Right").encode()).ljust(16))
	loop = 0
	time.sleep(0.5)
	while loop < 4:
		while count < 5:
			s.send((("1.2").encode()).ljust(16))
			count += 1
			time.sleep(0.5)
		count = 0
		s.send((("Left").encode()).ljust(16))
		loop += 1
		time.sleep(0.5)
	s.send((("Left").encode()).ljust(16))
	time.sleep(0.5)

def move2():
	print("enter function_2")
	s.send((("0.0").encode()).ljust(16))
	loop = 0
	count = 0
	time.sleep(0.5)
	while loop < 4:
		while count < 5:
			s.send((("1.2").encode()).ljust(16))
			count += 1
			time.sleep(0.5)
		count = 0
		s.send((("Right").encode()).ljust(16))
		time.sleep(0.5)
		loop += 1
	time.sleep(0.5)

def move3():
	print("enter function_3")
	s.send((("0.0").encode()).ljust(16))
	count = 0
	time.sleep(0.5)
	while count < 5:
		s.send((("1.4").encode()).ljust(16))
		count += 1
		time.sleep(0.5)
	count = 0
	s.send((("Left").encode()).ljust(16))
	time.sleep(0.5)
	while count < 9:
		s.send((("1.5").encode()).ljust(16))
		count += 1
		time.sleep(0.5)
	s.send((("Left").encode()).ljust(16))
	time.sleep(0.5)
	s.send((("Left").encode()).ljust(16))
	time.sleep(0.5)
	count = 0
	while count < 9:
		s.send((("1.5").encode()).ljust(16))
		count += 1
		time.sleep(0.5)
	s.send((("Right").encode()).ljust(16))
	time.sleep(0.5)
	count = 0
	while count < 5:
		s.send((("1.4").encode()).ljust(16))
		count += 1
		time.sleep(0.5)

	s.send((("Right").encode()).ljust(16))
	time.sleep(0.5)
	s.send((("Right").encode()).ljust(16))
	time.sleep(0.5)

def move4():
	print("enter function_4")
	s.send((("0.0").encode()).ljust(16))
	time.sleep(0.5)
	count = 0

	s.send((("Right").encode()).ljust(16))
	time.sleep(0.5)

	while count < 4:
		s.send((("1.5").encode()).ljust(16))
		count += 1
		time.sleep(0.5)
	count = 0
	s.send((("Left").encode()).ljust(16))
	time.sleep(0.5)
	while count < 9:
		s.send((("1.5").encode()).ljust(16))
		count += 1
		time.sleep(0.5)
	count = 0
	s.send((("Right").encode()).ljust(16))
	time.sleep(0.5)
	s.send((("Right").encode()).ljust(16))
	time.sleep(0.5)

	while count < 9:
		s.send((("1.5").encode()).ljust(16))
		count += 1
		time.sleep(0.5)
	count = 0
	s.send((("Right").encode()).ljust(16))
	time.sleep(0.5)
	while count < 4:
		s.send((("1.5").encode()).ljust(16))
		count += 1
		time.sleep(0.5)
	
	s.send((("Right").encode()).ljust(16))
	time.sleep(0.5)
	
def move5():
	print("enter function_5")
	s.send((("0.0").encode()).ljust(16))
	time.sleep(0.5)
	count = 0

	while count < 5:
		s.send((("1.4").encode()).ljust(16))
		time.sleep(0.5)
		count += 1
	count = 0
	s.send((("Right").encode()).ljust(16))
	time.sleep(0.5)
	while count < 4:
		s.send((("1.5").encode()).ljust(16))
		time.sleep(0.5)
		count += 1
	s.send((("Left").encode()).ljust(16))
	time.sleep(0.5)
	count = 0
	while count < 4:
		s.send((("1.5").encode()).ljust(16))
		time.sleep(0.5)
		count += 1
	count = 0
	s.send((("Right").encode()).ljust(16))
	time.sleep(0.5)
	s.send((("Right").encode()).ljust(16))
	time.sleep(0.5)

	while count < 4:
		s.send((("1.5").encode()).ljust(16))
		time.sleep(0.5)
		count += 1
	s.send((("Right").encode()).ljust(16))
	time.sleep(0.5)
	count = 0
	
	while count < 4:
		s.send((("1.5").encode()).ljust(16))
		time.sleep(0.5)
		count += 1
	count = 0
	s.send((("Left").encode()).ljust(16))
	time.sleep(0.5)
	
	while count < 5:
		s.send((("1.4").encode()).ljust(16))
		time.sleep(0.5)
		count += 1
	s.send((("Right").encode()).ljust(16))
	time.sleep(0.5)
	s.send((("Right").encode()).ljust(16))
	time.sleep(0.5)

def move6():
	print("enter function_6")
	s.send((("0.0").encode()).ljust(16))
	count = 0

	while count < 5:
		s.send((("1.4").encode()).ljust(16))
		count += 1
		time.sleep(0.5)

	s.send((("Left").encode()).ljust(16))
	time.sleep(0.5)

	s.send((("1.5").encode()).ljust(16))
	time.sleep(0.5)
	s.send((("Left").encode()).ljust(16))
	time.sleep(0.5)
	count = 0
	while count < 5:
		s.send((("1.5").encode()).ljust(16))
		count += 1
		time.sleep(0.5)
	
	s.send((("Right").encode()).ljust(16))
	time.sleep(0.5)
	s.send((("Right").encode()).ljust(16))
	time.sleep(0.5)
	count = 0
	while count < 5:
		s.send((("1.5").encode()).ljust(16))
		count += 1
		time.sleep(0.5)
	count = 0

	s.send((("Right").encode()).ljust(16))
	time.sleep(0.5)
	s.send((("1.5").encode()).ljust(16))
	time.sleep(0.5)
	s.send((("Right").encode()).ljust(16))
	time.sleep(0.5)

	count = 0
	while count < 5:
		s.send((("1.4").encode()).ljust(16))
		count += 1
		time.sleep(0.5)

	s.send((("Right").encode()).ljust(16))
	time.sleep(0.5)
	s.send((("Right").encode()).ljust(16))
	time.sleep(0.5)

def move7():
	print("enter function_7")
	s.send((("0.0").encode()).ljust(16))
	count = 0
	
	while count < 5:
		s.send((("1.4").encode()).ljust(16))
		count += 1
		time.sleep(0.5)

	s.send((("Left").encode()).ljust(16))
	time.sleep(0.5)
	count = 0
	while count < 6:
		s.send((("1.5").encode()).ljust(16))
		time.sleep(0.5)
		count += 1
	
	s.send((("Left").encode()).ljust(16))
	time.sleep(0.5)
	count = 0
	loop = 0
	s.send((("1.5").encode()).ljust(16))
	time.sleep(0.5)
	s.send((("1.5").encode()).ljust(16))
	time.sleep(0.5)
	while loop < 4:
		while count < 4:
			s.send((("1.5").encode()).ljust(16))
			count += 1
			time.sleep(0.5)
		s.send((("Right").encode()).ljust(16))
		time.sleep(0.5)
		count = 0
		loop += 1
	
	s.send((("Left").encode()).ljust(16))
	time.sleep(0.5)
	s.send((("Left").encode()).ljust(16))
	time.sleep(0.5)
	s.send((("1.5").encode()).ljust(16))
	time.sleep(0.5)
	s.send((("1.5").encode()).ljust(16))
	time.sleep(0.5)
	s.send((("Right").encode()).ljust(16))
	time.sleep(0.5)
	
	count = 0
	while count < 6:
		s.send((("1.5").encode()).ljust(16))
		count += 1
		time.sleep(0.5)
	count = 0
	s.send((("Right").encode()).ljust(16))
	time.sleep(0.5)
	while count < 5:
		s.send((("1.4").encode()).ljust(16))
		count += 1
		time.sleep(0.5)

	s.send((("Right").encode()).ljust(16))
	time.sleep(0.5)
	s.send((("Right").encode()).ljust(16))
	time.sleep(0.5)

s.send((("Tony").encode()).ljust(16))
print("Tony")
time.sleep(1)
s.send((("0.0").encode()).ljust(16))
print("0.0")
time.sleep(1)
s.send((("0.0").encode()).ljust(16))
print("0.0")
time.sleep(5)

while True:
	move7()
