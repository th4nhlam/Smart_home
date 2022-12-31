import smbus2
import time
import json
import requests
import pyrebase
import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)
led1=26
led2=5
led3=6

#GPIO.setup(led2, GPIO.OUT)
#GPIO.setup(led3, GPIO.OUT)
# Define some constants from the datasheet

DEVICE     = 0x23 # Default device I2C address

POWER_DOWN = 0x00 # No active state
POWER_ON   = 0x01 # Power on
RESET      = 0x07 # Reset data register value

# Start measurement at 4lx resolution. Time typically 16ms.
CONTINUOUS_LOW_RES_MODE = 0x13
# Start measurement at 1lx resolution. Time typically 120ms
CONTINUOUS_HIGH_RES_MODE_1 = 0x10
# Start measurement at 0.5lx resolution. Time typically 120ms
CONTINUOUS_HIGH_RES_MODE_2 = 0x11
# Start measurement at 1lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_HIGH_RES_MODE_1 = 0x20
# Start measurement at 0.5lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_HIGH_RES_MODE_2 = 0x21
# Start measurement at 1lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_LOW_RES_MODE = 0x23

#bus = smbus.SMBus(0) # Rev 1 Pi uses 0
bus = smbus2.SMBus(1)  # Rev 2 Pi uses 1
time.sleep(1);

def convertToNumber(data):
  # Simple function to convert 2 bytes of data
  # into a decimal number. Optional parameter 'decimals'
  # will round to specified number of decimal places.
  result=(data[1] + (256 * data[0])) / 1.2
  return (result)

def readLight(addr=DEVICE):
  # Read data from I2C interface
  
  data = bus.read_i2c_block_data(addr,CONTINUOUS_HIGH_RES_MODE_2,10);
  return convertToNumber(data)

state=0
def main():
  global state
  
  while True:
    print(state)
    lightLevel=readLight()
    print("Light Level : " + format(lightLevel,'.2f') + " lx")
    if(lightLevel>30 and state==1):
      requests.get("http://127.0.0.1:8000/led1/off/")
      state=0
      print("tat den")
    elif(lightLevel<30 and state==0):
      requests.get("http://127.0.0.1:8000/led1/on/")
      # sleep(3)
      # requests.get("http://127.0.0.1:8000/led2/off/")
      # sleep(3)
      # requests.get("http://127.0.0.1:8000/led3/off/")
      # sleep(3)
      state=1
      print("bat den")

    sleep(1)
    

if __name__=="__main__":
   main()