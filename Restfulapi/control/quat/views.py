from django.shortcuts import render
import RPi.GPIO as GPIO
from django.http import HttpResponse
from time import sleep
# Create your views here.
GPIO.setmode(GPIO.BCM)
in1=17
in2=27
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)

def turnOn(request):
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    return HttpResponse('')

def turnOff(request):
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    return HttpResponse('')