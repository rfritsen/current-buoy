# Expanding on read_register to get accurate calculation for compass heading

# Import external packages
import smbus
from time import sleep
import math
from gps import *

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

# Initialize Magnetometer
# Write to Configuration Register A, B, and Mode register.

def Magnetometer_Init():
    bus.write_byte_data(Device_Address, Register_A, 0x70)
    bus.write_byte_data(Device_Address, Register_B, 0xa0)
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


x = read_raw_data(X_axis_H)
z = read_raw_data(Z_axis_H)
y = read_raw_data(Y_axis_H)
jc_rad_dec     = -.1844813 # JC radian declination. 
az = 0
calc = "base"

if x < 0:
    az = 180 - (math.atan2(y, x))*(180/pi) + jc_rad_dec
    calc = "Calc 1"
elif x > 0 and y<0:
    az = -(math.atan2(y,x))*(180/pi) + jc_rad_dec
    calc = "Calc 2"
elif x>0 and y>0:
    az = 360-(math.atan2(y,x))*(180/pi) + jc_rad_dec
    calc = "Calc 3"
else:
    az = "Something else"

# heading = math.atan2(y, x)

#     if(heading > 2*pi):
#         heading = heading - 2*pi
#     if(heading <0):
#         heading = heading + 2*pi
#     heading_angle = int(heading* 180/pi)


print('X\tY\tZ\tCompass\tCalc')
print(
    x, "\t",
    y, "\t",
    z, "\t",
    az, "\t", 
    calc
)
