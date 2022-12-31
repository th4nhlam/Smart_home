from django.shortcuts import render
from gpiozero import AngularServo
from time import sleep
from django.http import HttpResponse
from gpiozero.pins.pigpio import PiGPIOFactory
pigpio_factory = PiGPIOFactory()
servo=AngularServo(21, min_pulse_width=0.0006, max_pulse_width=0.0023,pin_factory=pigpio_factory)


    
# Create your views here.
def opendoor(request):
    servo.angle=10
    return HttpResponse('')

def closedoor(request):
    servo.angle=90
    return HttpResponse('')
