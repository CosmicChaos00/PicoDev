from imu import MPU6050
from time import sleep
import time
from machine import Pin, I2C
from vectorMagnitude import VectorMagnitude 
import isPlayerMoving
import Pico
import wifiLogin
import machine
import utime
import urequests
import gc
import updatePico

led = machine.Pin("LED", machine.Pin.OUT)
def toggle_led():
    # Turn on the LED
    led.value(1)  # 1 = ON, 0 = OFF
    
    # Wait for a short duration (e.g., 1 second)
    utime.sleep(1)
    
    # Turn off the LED
    led.value(0)

dev_ID = Pico.get_DeviceId()


wifiLogin.wifi_Login()
gc.collect()
updatePico.update()
#uploadDeviceID.uploadDevice()

server_url = 'http://192.168.1.140:3000/upload'

# set the linear acceleration range to +/- 2g's
MPU6050.acc_range = 0

# set the gyroscope range to +/- 500 degress/second 
MPU6050.gyro_range= 1


i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
imu = MPU6050(i2c)

start_time = time.ticks_ms() #get intial time

while True:
    ax = round(imu.accel.x, 1)
    ay = round(imu.accel.y, 1)
    az = round(imu.accel.z, 1)
    gx = round(imu.gyro.x, 1)  # Assuming you also want these rounded to one decimal
    gy = round(imu.gyro.y, 1)
    gz = round(imu.gyro.z, 1)
    current_time = time.ticks_ms()
    elapsed_time = time.ticks_diff(current_time, start_time)
    
    
    toggle_led()
    vectInstance = VectorMagnitude(ax, ay, az)
    magnitude = vectInstance.getVectorMagnitude()
    theta = vectInstance.getTheta()
    phi = vectInstance.getPhi()
    
    
    data = {'data': [dev_ID, ax, ay, az, gx, gy, gz,magnitude,theta,phi]}
    

    # Check if vector magnitude is adequate and call the method correctly
    if magnitude >= 2:
        try:
            response = urequests.post(server_url, json=data)
            response.close()
            print('Data sent successfully')
        except Exception as e:
            print('Error sending data:', e)
    print("Accelerometer values:", ax, ay, az)    
    print(vectInstance.getVectorMagnitude())
    

    time.sleep(1)

