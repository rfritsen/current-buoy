'''
GPS data for export to CSV
'''

# Import packages
import serial               #import serial pacakge
from time import sleep
import webbrowser           #import package for opening link in browser
import sys                  #import system package

# Variables
ser = serial.Serial ("/dev/ttyS0")              #Open port with baud rate

# Read serial port data from GPS unit
# Take 5min snapshot

try:
    while True:
        received_data = (ser.readline())
    print("NMEA raw info: ", received_data)

except KeyboardInterrupt:
    webbrowser.open(map_link)        #open current position information in google map
    sys.exit(0)

# Convert NMEA string to structured data

# Write GPS positional data to 