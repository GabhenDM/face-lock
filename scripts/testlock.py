import serial
import sys



arduino = serial.Serial('/dev/cu.usbmodem14101',9600)


if __name__ == '__main__':
	print(sys.argv[1])
	if sys.argv[1] == "on":
		print("Ligando")
#		arduino.write(b'A')
	elif sys.argv[1] == "off":
		print("Desligando")
#		arduino.write(b'D')
