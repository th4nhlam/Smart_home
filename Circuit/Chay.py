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
from gpiozero import AngularServo
from time import sleep
from gpiozero import Buzzer
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import TonalBuzzer
from gpiozero.tones import Tone
# Define some constants from the datasheet
pigpio_factory = PiGPIOFactory()

GPIO.setmode(GPIO.BCM)

# in1=17
# in2=27
# GPIO.setup(in1, GPIO.OUT)
# GPIO.setup(in2, GPIO.OUT)
config = {
  "apiKey": "xpFpWOU99M28itFV7EiXuBUeMPe4SDUF8a90W3Lp",
  "authDomain": "nha-thong-minh-pfiev.firebaseapp.com",
  "databaseURL": "https://nha-thong-minh-pfiev-default-rtdb.asia-southeast1.firebasedatabase.app/",
  "storageBucket": "nha-thong-minh-pfiev.appspot.com"
}
fb= pyrebase.initialize_app(config)
db=fb.database();

dhtDevice = adafruit_dht.DHT11(16)
buzz=TonalBuzzer(22)
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
servo=AngularServo(21, pin_factory=pigpio_factory)

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
  return 0,0
    
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
    return value
  
v1 = ["G4", "G4", "G4", "D4", "E4", "E4", "D4"]
v2 = ["B4", "B4", "A4", "A4", "G4"]
v3 = ["D4", "G4", "G4", "G4", "D4", "E4", "E4", "D4"]

song = [v1,v2,v3,v2]
def converttoCelcius(f):
  return (f-32)/1.8
state=0
def main():
  global state
  while True:
    temp=0
    hum=0
    lightLevel=readLight()
    temp, hum=DHTread()
    gas=Arduinoread()
    
    if(temp!=0 and hum!=0):
      data={
        "Lightlevel": format(lightLevel,'.2f'),
        "Hum": hum,
        "Temp": temp,
        "Gas": gas
      }
    else:
      data={
        "Lightlevel": format(lightLevel,'.2f'),
        "Gas": gas
      }


    db.child().update(data)
    if(gas>100):
      requests.get("http://127.0.0.1:8000/cua/open/")
      # GPIO.output(in1, GPIO.HIGH)
      # GPIO.output(in2, GPIO.LOW)
      requests.get("http://127.0.0.1:8000/quat/on/")
      for verse in song:
        for note in verse:
          buzz.play(note)
          sleep(0.4)
          buzz.stop()
          sleep(0.1)
        sleep(0.2)
    else: 
      requests.get("http://127.0.0.1:8000/cua/close/")
      requests.get("http://127.0.0.1:8000/quat/off/")
      buzz.stop()

    if(lightLevel<30 and state==0):
      requests.get("http://127.0.0.1:8000/led1/on/")
      requests.get("http://127.0.0.1:8000/led2/on/")
      requests.get("http://127.0.0.1:8000/led3/on/")
      state=1
      print("bat den")
    elif(lightLevel>30 and state==1):
      requests.get("http://127.0.0.1:8000/led1/off/")
      requests.get("http://127.0.0.1:8000/led2/off/")
      requests.get("http://127.0.0.1:8000/led3/off/")

      state=0
      print("tat den")  


if __name__=="__main__":
   main()
