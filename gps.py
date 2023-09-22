import serial
import pynmea2

ser = serial.Serial('/dev/ttyS0', 9600, timeout=1)

try:
    while True:
        sentence = ser.readline().decode('utf-8')
        
        if sentence.startswith('$GPGGA'):
            try:
                msg = pynmea2.parse(sentence)
                
                if msg.timestamp is not None:
                    latitude = msg.latitude
                    longitude = msg.longitude
                    
                    print(f"Latitude: {latitude}, Longitude: {longitude}")
                    
            except pynmea2.ParseError as e:
                print(f"Error parsing NMEA sentence: {str(e)}")
            
except KeyboardInterrupt:
    print("\nGPS data printing stopped.")
