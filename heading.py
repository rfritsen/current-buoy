'''
Current Monitor (aka "Velociraptor")
Ryan Fritsen | April 2024

Description: 
# Runs automatically on powerup.
# Finds compass heading and GPS location every 5 minutes 
# Prints to a <TODO add data structure>
# Using Python HMC5883L interface
# Adapted for use with BN-880 magnetometer, Raspberry Pi and Python
# Designed for use on a floating buoy in Jersey City, NJ 


Credits:
# For compass heading: Original code at www.electronicwings.com/raspberry-pi/triple-axis-magnetometer-hmc5883l-interfacing-with-raspberry-pi
# For GPS position: Original code at 

To install packages:
# smbus: TODO
# time: TODO
# math: TODO

To find device locations on bus and register. Use terminal.
# Find magnetometer location: i2cdetect -y 1

For documentation on reading the byte data: TODO
'''

# Import external packages
import smbus
from time import sleep
import math
from gps import *

################################################################################
# Foundational Functions

# Set addresses of registers. These are used for: TODO
Register_A     = 0
Register_B     = 0x01
Register_mode  = 0x02

X_axis_H       = 0x03
Z_axis_H       = 0x05
Y_axis_H       = 0x07
declination    = .96586521 # in radians?
jc_rad_dec     = -.1844813 # JC radian declination. 
pi             = 3.14159265359

# Initialize magnetometer. 
# TODO - Fix description. Tells magnetometer what register to communicate with.
# TODO - How to pick the register addresses?
def Magnetometer_Init():
    # Write to Configuration Register A. TODO what is this?
    bus.write_byte_data(Device_Address, Register_A, 0x70)
    # Write to Configuration Register B for gain. TODO what is this?
    bus.write_byte_data(Device_Address, Register_B, 0xa0)
    # Write to Mode register. TODO what is this?
    bus.write_byte_data(Device_Address, Register_mode, 0)

# Read raw 16-bit values from magnetometer
# Concatenate higher and lower value. TODO what do higher/lower represent?
# Get signed value from module TODO what does signed value mean?
# TODO how did we get the value calculations?
def read_raw_data(addr):
    high = bus.read_byte_data(Device_Address, addr)
    low = bus.read_byte_data(Device_Address, addr+1)
    value = ((high << 8) | low)
    if(value > 32768):
        value = value - 65536
    return value

# TODO what does this line do?
gpsd = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE)

#############################################################################
# Print values from magnetometer and GPS

# Initialize Magnetometer
# Read X, Y, Z data from magnetometer
# Calculate compass heading in degrees
# Write compass heading to terminal
# TODO Fix compass heading math

bus = smbus.SMBus(1) 
Device_Address = 0x1e # Device address. TODO How do we find this?
Magnetometer_Init()
print('heading\tlatitude\tlongitude') # TODO
while True:
    # Compass
    x = read_raw_data(X_axis_H)
    z = read_raw_data(Z_axis_H)
    y = read_raw_data(Y_axis_H)

    heading = math.atan2(y, x) + jc_rad_dec

    if(heading > 2*pi):
        heading = heading - 2*pi
    if(heading <0):
        heading = heading + 2*pi
    heading_angle = int(heading* 180/pi)
    
    # GPS
    report = gpsd.next()
    if report ['class'] == 'TPV':
        print(
            heading_angle, "\t",
            getattr(report, 'lat', 0.0), "\t",
            getattr(report, 'lon', 0.0), "\t"
        )
    sleep(2)

#############################################################################
'''
# Read values from magnetometer

# TODO What does bus function do?
# TODO How to find device address?
bus = smbus.SMBus(1) 
Device_Address = 0x1e # Device address. TODO How do we find this?

# Initialize Magnetometer
# Read X, Y, Z data from magnetometer
# Calculate compass heading in degrees
# Write compass heading to terminal
# TODO Fix compass heading math

Magnetometer_Init()
print("Reading heading angle")
while True: # TODO Fix math so heading angle is accurate
    x = read_raw_data(X_axis_H)
    z = read_raw_data(Z_axis_H)
    y = read_raw_data(Y_axis_H)

    heading = math.atan2(y, x) + declination

    if(heading > 2*pi):
        heading = heading - 2*pi
    if(heading <0):
        heading = heading + 2*pi
    heading_angle = int(heading* 180/pi)

    print("Heading angle: %d" %heading_angle, "Latitude: ", "Longitude: ")
    sleep(1)
'''
#############################################################################
'''
# Read values from GPS

# TODO What does this do?
# 

print('latitude\tlongitude') # TODO

try:
    while True:
        report = gpsd.next()
        if report ['class'] == 'TPV':
            print(
                getattr(report, 'lat', 0.0), "\t",
                getattr(report, 'lon', 0.0), "\t"
                )
            time.sleep(1)
except (KeyboardInterrupt, SystemExit):
    print("Done. \nExiting.")
    '''