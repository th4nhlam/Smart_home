from django.shortcuts import render
import RPi.GPIO as GPIO
from django.http import HttpResponse
from time import sleep
# Create your views here.
LED_PIN = 6
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
pi_pwm = GPIO.PWM(LED_PIN,1000)		#create PWM instance with frequency
pi_pwm.start(0)
def turnOn(request):
    
    for duty in range(0,101,1):
        pi_pwm.ChangeDutyCycle(duty) #provide duty cycle in the range 0-100
        sleep(0.01)
    sleep(0.5)
    return HttpResponse('')


def turnOff(request):
    
    for duty in range(100,-1,-1):
        pi_pwm.ChangeDutyCycle(duty)
        sleep(0.01)
    sleep(0.5)
    return HttpResponse('')