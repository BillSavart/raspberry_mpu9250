import socket
import time
import random

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

			#random help
			ran = random.randint(1,100)
			if ran == 5:
				help_me()
			elif ran == 10:
				not_help()

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

			#random help
			ran = random.randint(1,100)
			if ran == 5:
				help_me()
			elif ran == 10:
				not_help()

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
		
		#random help
		ran = random.randint(1,100)
		if ran == 10:
			help_me()
		elif ran == 20:
			not_help()
		
	count = 0
	s.send((("Left").encode()).ljust(16))
	time.sleep(0.5)
	while count < 9:
		s.send((("1.5").encode()).ljust(16))
		count += 1
		time.sleep(0.5)

		#random help
		ran = random.randint(1,100)
		if ran == 10:
			help_me()
		elif ran == 30:
			not_help()

	s.send((("Left").encode()).ljust(16))
	time.sleep(0.5)
	s.send((("Left").encode()).ljust(16))
	time.sleep(0.5)
	count = 0
	while count < 9:
		s.send((("1.5").encode()).ljust(16))
		count += 1
		time.sleep(0.5)

		#random help
		ran = random.randint(1,100)
		if ran == 10:
			not_help()
		elif ran == 30:
			help_me()

	s.send((("Right").encode()).ljust(16))
	time.sleep(0.5)
	count = 0
	while count < 5:
		s.send((("1.4").encode()).ljust(16))
		count += 1
		time.sleep(0.5)
		
		#random help
		ran = random.randint(1,100)
		if ran == 10:
			not_help()
		elif ran == 30:
			help_me()

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

		#random help
		ran = random.randint(1,100)
		if ran == 10:
			not_help()
		elif ran == 2:
			help_me()

	count = 0
	s.send((("Left").encode()).ljust(16))
	time.sleep(0.5)
	while count < 9:
		s.send((("1.5").encode()).ljust(16))
		count += 1
		time.sleep(0.5)
	
		#random help
		ran = random.randint(1,100)
		if ran == 10:
			help_me()
		elif ran == 20:
			not_help()

	count = 0
	s.send((("Right").encode()).ljust(16))
	time.sleep(0.5)
	s.send((("Right").encode()).ljust(16))
	time.sleep(0.5)

	while count < 9:
		s.send((("1.5").encode()).ljust(16))
		count += 1
		time.sleep(0.5)

		#random help
		ran = random.randint(1,100)
		if ran == 10:
			help_me()
		elif ran == 20:
			not_help()

	count = 0
	s.send((("Right").encode()).ljust(16))
	time.sleep(0.5)
	while count < 4:
		s.send((("1.5").encode()).ljust(16))
		count += 1
		time.sleep(0.5)

		#random help
		ran = random.randint(1,100)
		if ran == 10:
			help_me()
		elif ran == 30:
			not_help()
	
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

		#random help
		ran = random.randint(1,100)
		if ran == 10:
			help_me()
		elif ran == 30:
			not_help()

	count = 0
	s.send((("Right").encode()).ljust(16))
	time.sleep(0.5)
	while count < 4:
		s.send((("1.5").encode()).ljust(16))
		time.sleep(0.5)
		count += 1

		#random help
		ran = random.randint(1,100)
		if ran == 10:
			not_help()
		elif ran == 30:
			help_me()

	s.send((("Left").encode()).ljust(16))
	time.sleep(0.5)
	count = 0
	while count < 4:
		s.send((("1.5").encode()).ljust(16))
		time.sleep(0.5)
		count += 1

		#random help
		ran = random.randint(1,100)
		if ran == 10:
			help_me()
		elif ran == 20:
			not_help()

	count = 0
	s.send((("Right").encode()).ljust(16))
	time.sleep(0.5)
	s.send((("Right").encode()).ljust(16))
	time.sleep(0.5)

	while count < 4:
		s.send((("1.5").encode()).ljust(16))
		time.sleep(0.5)
		count += 1
		
		#random help
		ran = random.randint(1,100)
		if ran == 10:
			not_help()
		elif ran == 20:
			help_me()

	s.send((("Right").encode()).ljust(16))
	time.sleep(0.5)
	count = 0
	
	while count < 4:
		s.send((("1.5").encode()).ljust(16))
		time.sleep(0.5)
		count += 1

		#random help
		ran = random.randint(1,100)
		if ran == 10:
			help_me()
		elif ran == 30:
			not_help()

	count = 0
	s.send((("Left").encode()).ljust(16))
	time.sleep(0.5)
	
	while count < 5:
		s.send((("1.4").encode()).ljust(16))
		time.sleep(0.5)
		count += 1

		#random help
		ran = random.randint(1,100)
		if ran == 10:
			not_help()
		elif ran == 30:
			help_me()

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

		#random help
		ran = random.randint(1,100)
		if ran == 10:
			not_help()
		elif ran == 20:
			help_me()

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

		#random help
		ran = random.randint(1,100)
		if ran == 10:
			help_me()
		elif ran == 20:
			not_help()
	
	s.send((("Right").encode()).ljust(16))
	time.sleep(0.5)
	s.send((("Right").encode()).ljust(16))
	time.sleep(0.5)
	count = 0
	while count < 5:
		s.send((("1.5").encode()).ljust(16))
		count += 1
		time.sleep(0.5)

		#random help
		ran = random.randint(1,100)
		if ran == 10:
			help_me()
		elif ran == 20:
			not_help()

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
		
		#random help
		ran = random.randint(1,100)
		if ran == 10:
			help_me()
		elif ran == 20:
			not_help()

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

		#random help
		ran = random.randint(1,100)
		if ran == 10:
			not_help()
		elif ran == 20:
			help_me()

	s.send((("Left").encode()).ljust(16))
	time.sleep(0.5)
	count = 0
	while count < 6:
		s.send((("1.5").encode()).ljust(16))
		time.sleep(0.5)
		count += 1

		#random help
		ran = random.randint(1,100)
		if ran == 10:
			help_me()
		elif ran == 20:
			not_help()
	
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

			#random help
			ran = random.randint(1,100)
			if ran == 10:
				not_help()
			elif ran == 20:
				help_me()

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

		#random help
		ran = random.randint(1,100)
		if ran == 10:
			help_me()
		elif ran == 20:
			not_help()

	count = 0
	s.send((("Right").encode()).ljust(16))
	time.sleep(0.5)
	while count < 5:
		s.send((("1.4").encode()).ljust(16))
		count += 1
		time.sleep(0.5)

		#random help
		ran = random.randint(1,100)
		if ran == 10:
			not_help()
		elif ran == 20:
			help_me()

	s.send((("Right").encode()).ljust(16))
	time.sleep(0.5)
	s.send((("Right").encode()).ljust(16))
	time.sleep(0.5)

def help_me():
	count = 0
	print("enter help_condition")

	ra = random.randint(1,8)
	
	if ra == 1:
		temp = 3

	elif ra == 2:
		temp = 4

	elif ra == 3:
		temp = 5

	elif ra == 4:
		temp = 6

	elif ra == 5:
		temp = 7

	elif ra == 6:
		temp = 8

	elif ra == 7:
		temp = 9

	else:
		temp = 10

	while count < 10:
		s.send((("HELP").encode()).ljust(16))
		time.sleep(0.5)
		count += 1
	count = 0

	ra = random.randint(1,4)
	if ra == 1:
		temp = 6

	elif ra == 2:
		temp = 10

	elif ra == 3:
		temp = 14

	else:
		temp = 20

	while count < temp:
		s.send((("HELP2").encode()).ljust(16))
		time.sleep(0.5)
		count += 1

def not_help():
	count = 0
	print("enter not_really_need_help")

	rand = random.randint(1,9)

	if rand == 1:
		tmp = 2
	elif rand == 2:
		tmp = 3
	elif rand == 3:
		tmp = 4
	elif rand == 4:
		tmp = 5
	elif rand == 5:
		tmp = 6
	elif rand == 6:
		tmp = 7
	elif rand == 7:
		tmp = 8
	elif rand == 8:
		tmp = 9
	else:
		tmp = 10

	while count < tmp:
		s.send((("HELP").encode()).ljust(16))
		time.sleep(0.5)
		count += 1

s.send((("Stark").encode()).ljust(16))
print("Stark")
time.sleep(1)
s.send((("num2").encode()).ljust(16))
time.sleep(1)
s.send((("0.0").encode()).ljust(16))
print("0.0")
time.sleep(1)
s.send((("0.0").encode()).ljust(16))
print("0.0")

print("click the map, hurry up!!")
time.sleep(10)

while True:
	r = random.randint(1,7)
	if r == 1:
		move1()
	elif r == 2:
		move2()
	elif r == 3:
		move3()
	elif r == 4:
		move4()
	elif r == 5:
		move5()
	elif r == 6:
		move6()
	else:
		move7()
