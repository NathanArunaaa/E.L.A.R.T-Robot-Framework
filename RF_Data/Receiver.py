import serial

ser = serial.Serial('COM3', 57600)  


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
