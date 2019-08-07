import smbus
import time
import math
import socket
import numpy as np
import multiprocessing as mp

HOST = '192.168.68.100'
PORT = 8888

# Register
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

# Variable
start = 0  #for time interval
start_warning_time = 0
help_flag = False
real_bes = 0
real_gyro = 0
stop_key = False
turning_flag = False

#f_bes = open('./normal_walk.txt', 'a')
#f_gyro = open('no_turn' + str(index) + '.txt', 'a')

def read_byte(reg):
	return bus.read_byte_data(address, reg)

def read_word(reg):
	h = bus.read_byte_data(address, reg)
	l = bus.read_byte_data(address, reg+1)
	value = (h << 8) + l
	return value

def read_word_2c(reg):
	val = read_word(reg)
	if (val >= 0x8000):
		return -((65535 - val) + 1)
	else:
		return val

def read_gyro():
	xout = read_word_2c(0x43)
	yout = read_word_2c(0x45)
	zout = read_word_2c(0x47)
	return xout

def read_bes_x():
	bes_x = read_word_2c(0x3b)
	bes_y = read_word_2c(0x3d)
	bes_z = read_word_2c(0x3f)

	bes_x_ska = bes_x / 16384.0 * 9.8
	return bes_x_ska

def read_bes_z():
	bes_x = read_word_2c(0x3b)
	bes_y = read_word_2c(0x3d)
	bes_z = read_word_2c(0x3f)

	bes_z_ska = bes_z / 16384.0 * 9.8
	return bes_z_ska

def get_bes(mutex, distance, dis_flag):
	global real_bes
	global stop_key
	bes_arr = []
	global f_bes
	while True:
		temp_data = read_bes_z()
		bes_arr.append(temp_data)
#		f_bes.write(str(temp_data)+'\n')
		if len(bes_arr) >= 500:
			real_bes = np.std(bes_arr)
			print('real_bes: ', real_bes)
			if real_bes <= 0.3 and real_bes > 0:
				pass
		#	elif real_bes > 0.5 and real_bes < 2:
		#		mutex.acquire()
		#		distance.value = distance.value + 0.1
		#		mutex.release()
			else:
				mutex.acquire()
				distance.value = distance.value + 0.2
				mutex.release()
			bes_arr = []
			dis_flag.value = 1

		if stop_key == True:
			break

def check_turning(mutex, turn, turn_flag):
	global real_gyro
	global stop_key
	global f_bes
	#start = 0
	#gyro_arr = []

	while True:
	#	if start == 0:
	#		start = time.time()

	#	end = time.time()
	#	time_inter = end - start
#		print(time_inter)
		
	#	gyro_yout = read_gyro()
	#	turn.value = (gyro_yout * 250.0 * time_inter) / 131.0
		turn.value = read_gyro()
		turn_flag.value = 1
	#	start = end
	#	time.sleep(1)
		#print(mp.current_process())
	#	temp_data = (read_gyro() * 250.0) / 131.0
	#	gyro_arr.append(temp_data)
		#f_bes.write(str(temp_data)+'\n')
		
	#	if len(gyro_arr) >= 500:
	#		real_gyro = np.median(gyro_arr)
	#		print('gyro: ',real_gyro)
	#		if real_gyro >= -1500 and real_gyro <= 1000:
	#			mutex.acquire()
	#			turn.value = 0
	#			mutex.release()
	#		elif real_gyro < -1500:
	#			mutex.acquire()
	#			turn.value = turn.value + 1
	#			mutex.release()
	#		elif real_gyro > 1000:
				#mutex.acquire()
	#			turn.value = turn.value - 1
	#			mutex.release()
	#		else:
	#			pass
	#		turn_flag.value = 1
	#		gyro_arr = []
		if stop_key == True:
			break

#main
bus = smbus.SMBus(1) 
address = 0x68       # via i2cdetect
bus.write_byte_data(address, power_mgmt_1, 0)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.connect((HOST,PORT))

mutex = mp.Lock()

distance = mp.Value("d", 0)
turn = mp.Value("d", 0)

turn_flag = mp.Value("i", 0)
dis_flag = mp.Value("i", 0)

p = mp.Process(target=get_bes, args=(mutex, distance, dis_flag))
p1 = mp.Process(target=check_turning, args=(mutex, turn, turn_flag))
p.start()
p1.start()

try:
	while True:
		#check if falling
		bes_xout = read_bes_x()
		if bes_xout > -6.0:
			if start_warning_time == 0:
				start_warning_time = time.time()
			else:
				if time.time() - start_warning_time >= 5 and time.time() - start_warning_time < 10:
					#s.send(("HELP").ljust(16))
					print("HELP")
					help_flag = True
				elif time.time() - start_warning_time >= 10:
					#s.send(("HELP2").ljust(16))
					print("HELP2")
		else:
			start_warning_time = 0
			help_flag = False

		#send bes
		mutex.acquire()
		if (help_flag == False and dis_flag.value == 1) and turning_flag == False:
			temp_dis = str(distance.value)
			#s.send((temp_dis).ljust(16))
			print(temp_dis)
			distance.value = 0
			dis_flag.value = 0
		mutex.release()

		#send turning
		if help_flag == False and turn_flag.value == 1:
			mutex.acquire()
			bes_for_gyro = read_bes_z()
		#	turn.value = turn.value % 4
			turning_flag = True
			if turn.value >= -10000 and turn.value <= 10000:
				turning_flag = False
				#print("gyro: ",turn.value)
				#print("bes: ", bes_for_gyro)
				#s.send(("No Turn").ljust(16))
				#time.sleep(1)
				#data = s.recv(1024)
				#print(data)
			#	print("No Turn")
				#time.sleep(1)
				
			elif turn.value < -10000:
				#s.send(("Left").ljust(16))
				#data = s.recv(1024)
				#print(data)
				print("Left")
				#print("gyro: ", turn.value)
				#print("bes: ", bes_for_gyro)
				#time.sleep(1)
				
			#elif turn.value > :
				#s.send("Right")
				#data = s.recv(1024)
				#print(data)
				#s.send("Right")
				#data = s.recv(1024)
				#print(data)
			#	print("RightRight")
				
			else:
				#s.send(("Right").ljust(16))
				#data = s.recv(1024)
				#print(data)
				print("Right")
				#print("gyro: ",turn.value)
				#print("bes: ", bes_for_gyro)
				#time.sleep(1)
				
			turn.value = 0
			turn_flag.value = 0
			turing_flag = False
			mutex.release()
		#	print('')
finally:
	stop_key = True
	#s.close()
	print("close")
