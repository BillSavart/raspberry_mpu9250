import serial
import sys
ser = serial.Serial('/dev/ttyACM0',9600)
line = 0

while 1:
	try:
		print("Waiting For Signal~~~")
		response = ser.readline()
		response = bytes.decode(response)
		print("Signal: ",response)
		if(response == 'HELP\r\n'):
			print("HELP")
#			ser.write('QAQ')
		elif (response == "HELP2\r\n"):
			print("HELP2")
#			ser.write('XDDDDDD')
		else:
			print("NO Equal")
	except:
		print(line)
		print(sys.exc_info()[0])
		ser.close()
		break
ser.close()
