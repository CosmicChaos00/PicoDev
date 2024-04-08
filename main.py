from imu import MPU6050
from time import sleep
import time
from machine import Pin, I2C
import vectorMagnitude
import isPlayerMoving
import Pico
import deviceID
import scanForAP
import wifiLogin
import machine
import utime
led = machine.Pin("LED", machine.Pin.OUT)
def toggle_led():
    # Turn on the LED
    led.value(1)  # 1 = ON, 0 = OFF
    
    # Wait for a short duration (e.g., 1 second)
    utime.sleep(1)
    
    # Turn off the LED
    led.value(0)

# Call the function to toggle the LED
#get PICO manfacturimng ID
dev_ID = deviceID.get_DeviceId()
#scanForAP.scanNearbyAP()

#loggin to wifi

wifiLogin.wifi_Login()
        

# set the linear acceleration range to +/- 2g's
MPU6050.acc_range = 0

# set the gyroscope range to +/- 500 degress/second 
MPU6050.gyro_range= 1
print("This file has been updated by github")

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
imu = MPU6050(i2c)

start_time = time.ticks_ms() #get intial time
while True:
    ax=round(imu.accel.x,1)
    ay=round(imu.accel.y,1)
    az=round(imu.accel.z,1)
    gx=round(imu.gyro.x)
    gy=round(imu.gyro.y)
    gz=round(imu.gyro.z)
    current_time = time.ticks_ms()
    elapsed_time = time.ticks_diff(current_time, start_time)
    
    toggle_led()
    
    print("aX: {} aY: {} aZ: {}".format(ax,ay,az))
        #print("Vector Magnitude: {}".format(vectorMagnitude.getVectorMagnitude(ax,ay,az)))

        #print("gyroX: {} gyroY: {} gyroZ: {}".format( gx,gy,gz))
    time.sleep(2)

