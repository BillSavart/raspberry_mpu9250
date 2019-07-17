import socket
import time
HOST = '192.168.68.100'
PORT = 8888

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST,PORT))

count = 0
help_condition = False
help_num = 0

try:
	while True:
		if help_condition == False:
			if count % 5 == 0:
				cmd = "Right"
			elif count == 21:
				help_condition = True
			else:
				cmd = "No Turn"

			s.send(cmd)
			data = s.recv(1024)
			print(data)
			s.send("0.2")
			data = s.recv(1024)
			print(data)
			count = count + 1
		else:
                        if help_num < 5:
			    cmd = "HELP"
			    s.send(cmd)
			    data = s.recv(1024)
			    print(data)
			    help_num += 1

			if help_num == 5:
				cmd = "HELP2"
				s.send(cmd)
				data = s.recv(1024)
				print(data)
			elif help_num == 8:
				help_condition = False
				count = 0
				help_num = 0
			else:
				pass
		time.sleep(1)
finally:
	s.close()
	print('close')
