from serial import Serial

port = '/dev/tty.usbserial-D30F08HK'
baud_rate = 57600

ser = Serial(port, baud_rate)

while True:
    command = ser.readline().decode().strip()  
    if command == 'LEFT':
        print("LEFT")
        pass
    
    elif command == 'Right':
        print("RIGHT")
        pass
    
    elif command == 'FORWARD':
        print("FORWARD")
        pass
    
    elif command == 'BACK':
        print("BACK")
        pass
