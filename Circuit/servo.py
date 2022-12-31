from gpiozero import AngularServo
from time import sleep
from gpiozero.pins.pigpio import PiGPIOFactory
pigpio_factory = PiGPIOFactory()
servo=AngularServo(21, min_pulse_width=0.0006, max_pulse_width=0.0023,pin_factory=pigpio_factory)


while(True):
    servo.angle=10
    print("servo 10")
    sleep(3)
    
    servo.angle=90
    print("servo 90")
    sleep(3)


    