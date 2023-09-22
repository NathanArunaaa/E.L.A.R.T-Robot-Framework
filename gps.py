import serial
import pynmea2  # Library to parse NMEA sentences
import datetime

# Define the serial port and baud rate
ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=1)

# Create a file to log GPS data
log_file = open("gps_log.txt", "a")

try:
    while True:
        # Read a line from the GPS module
        sentence = ser.readline().decode('utf-8')
        
        # Check if the sentence is a valid NMEA sentence
        if sentence.startswith('$GPGGA'):
            try:
                # Parse the NMEA sentence
                msg = pynmea2.parse(sentence)
                
                # Extract GPS data
                timestamp = datetime.datetime.combine(datetime.date.today(), msg.timestamp).strftime("%Y-%m-%d %H:%M:%S")
                latitude = msg.latitude
                longitude = msg.longitude
                altitude = msg.altitude
                
                # Log the data to a file
                log_entry = f"Time: {timestamp}, Latitude: {latitude}, Longitude: {longitude}, Altitude: {altitude} meters\n"
                log_file.write(log_entry)
                print(log_entry, end='')  # Print to console for debugging
                
            except pynmea2.ParseError as e:
                print(f"Error parsing NMEA sentence: {str(e)}")
            
        # You can add more conditions to parse other NMEA sentence types if needed
        
except KeyboardInterrupt:
    log_file.close()
    print("\nGPS logging stopped. Log file saved as 'gps_log.txt'")
