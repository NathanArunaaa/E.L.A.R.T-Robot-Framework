import serial
import time

ser = serial.Serial('/dev/ttyACM0', 9600)  # Use the correct USB port address

try:
    while True:
        line = ser.readline().decode('utf-8').strip()
        print(f"Sensor Value: {line}")
        time.sleep(1)

except KeyboardInterrupt:
    pass

finally:
    ser.close()