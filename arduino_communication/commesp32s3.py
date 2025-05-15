# INSTALL PYSERIAL FIRST!
# python3 -m pip install pyserial

# NOTE: Close Arduino IDE when running this code, since serial channel can only be accessed by one program at a time.

import serial
import time

# FILL IN THE PORT NAME DISPLAYED IN ARDUINO IDE
ser = serial.Serial('/dev/cu.usbmodem1101', 115200)

try:
	while True:
		# Send data to Pro Micro
		ser.write(b"Hello from Python!\n")
		
		# Read data from Pro Micro
		if ser.in_waiting > 0:
			line = ser.readline().decode('utf-8').rstrip()
			print(f"Received: {line}")
			
		time.sleep(1)
except KeyboardInterrupt:
	ser.close()
	print("Serial connection closed")