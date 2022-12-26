import smbus2
import time
import json
import requests
import pyrebase
import RPi.GPIO as GPIO
import board
import adafruit_dht
import serial
import psutil
from datetime import datetime, timezone
from gpiozero import Servo
# Define some constants from the datasheet
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
config = {
  "apiKey": "xpFpWOU99M28itFV7EiXuBUeMPe4SDUF8a90W3Lp",
  "authDomain": "nha-thong-minh-pfiev.firebaseapp.com",
  "databaseURL": "https://nha-thong-minh-pfiev-default-rtdb.asia-southeast1.firebasedatabase.app/",
  "storageBucket": "nha-thong-minh-pfiev.appspot.com"
}
fb= pyrebase.initialize_app(config)
db=fb.database();
DEVICE     = 0x23 # Default device I2C address

POWER_DOWN = 0x00 # No active state
POWER_ON   = 0x01 # Power on
RESET      = 0x07 # Reset data register value

dhtDevice = adafruit_dht.DHT11(board.D16)
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
servo = Servo(25)


def timestamp(dt):
    return dt.replace(tzinfo=timezone.utc).timestamp() * 1000

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

def DHTread():

  try:
    temperature = dhtDevice.temperature
    humidity = dhtDevice.humidity
    print("Temp: {:.1f} C    Humidity: {}% ".format(temperature, humidity))
    return temperature, humidity
  except RuntimeError as error:
    print(error.args[0])
    time.sleep(2.0)
    pass
    #continue
  except Exception as error:
    pass
    raise error
    
  time.sleep(2.0)
def Arduinoread():
  mytime = datetime.now()
  ser = serial.Serial('/dev/ttyACM0',9600)
  s = [0,1]
  read_serial=ser.readline()
  value = int (ser.readline(),16)
  #print(timestamp(datetime.now()) - timestamp(mytime))
  if (timestamp(datetime.now()) - timestamp(mytime) > 2000 ):
    mytime = datetime.now()
    print(value)
    return value
  

def converttoCelcius(f):
  return (f-32)/1.8
def main():

  while True:
    lightLevel=readLight()
    temp, hum=DHTread()
    gas=Arduinoread()
    
    
    data={
      "Lightlevel": format(lightLevel,'.2f'),
      "Hum": hum,
      "Temp": temp,
      "Gas": gas

    }

    db.child().update(data)
    if(gas>200):
      servo.max()
    else: 
      servo.min()
    time.sleep(2)

if __name__=="__main__":
   main()
