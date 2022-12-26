import serial
from datetime import datetime, timezone
from gpiozero import AngularServo
from time import sleep
import RPi.GPIO as GPIO
def timestamp(dt):
    return dt.replace(tzinfo=timezone.utc).timestamp() * 1000
import time
mytime = datetime.now()
ser = serial.Serial('/dev/ttyACM0',9600)
s = [0,1]
GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.OUT)
servo = AngularServo(25, min_angle=-180, max_angle=180)
while True:
    read_serial=ser.readline()
    value = int (ser.readline(),16)
    # print(timestamp(datetime.now()) - timestamp(mytime))
    if (timestamp(datetime.now()) - timestamp(mytime) > 2000 ):
        mytime = datetime.now()

    if (value>200):
        print(value)
        servo.max()
        sleep(2)
    else:
        print(value)
        servo.min()
        sleep(2)

        
    


