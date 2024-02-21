import serial
import time

ser = serial.Serial('/dev/ttyUSB0', 9600)  # Adjust port name as needed

try:
    while True:
        line = ser.readline().decode('utf-8').strip()
        print(f"Sensor Value: {line}")
        time.sleep(1)

except KeyboardInterrupt:
    pass

finally:
    ser.close()