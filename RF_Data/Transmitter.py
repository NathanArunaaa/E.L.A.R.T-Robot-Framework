import serial

ser = serial.Serial('COM3', 57600)  # Don't forget to change port 

while True:
   
    left_input = False  # Take these inputs from the hand held controller we will make
    right_input = True  # These will be changed to a float because a joystick is planned to be used
    front_input = False
    back_input = False
    
    if left_input == True:
        ser.write(b'LEFT\n')
        print ("LEFT")
        
    if right_input == True:
        ser.write(b'RIGHT\n')
        print ("RIGHT")
        
    if front_input == True:
        ser.write(b'FORWARD\n')
        print ("FORWARD")
	  
    if back_input == True:
        ser.write(b'BACK\n')
        print ("BACK")
        
        
        
		
    
    
    
    
	







 
