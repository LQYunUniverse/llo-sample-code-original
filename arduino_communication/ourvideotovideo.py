# INSTALL PYSERIAL FIRST!
# python3 -m pip install pyserial

# NOTE: Close Arduino IDE when running this code, since serial channel can only be accessed by one program at a time.

import serial
import time

# 请将这里的端口名称改为您在 Arduino IDE 中看到的端口名称
# 在 macOS 上通常是 /dev/cu.usbmodem* 或 /dev/tty.usbmodem*
ser = serial.Serial('/dev/cu.usbmodem101', 115200)

try:
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print(f"Received message: {line}")
        time.sleep(0.1)
except serial.SerialException as e:
    print("If you close Arduino IDE?")
      
except KeyboardInterrupt:
	ser.close()
	print("Serial connection closed")