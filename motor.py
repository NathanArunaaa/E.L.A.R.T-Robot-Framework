# Include the library files
import RPi.GPIO as GPIO
from time import sleep

# Include the motor control pins
ENA = 17
IN1 = 27
IN2 = 22

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(ENA,GPIO.OUT)
GPIO.setup(IN1,GPIO.OUT)
GPIO.setup(IN2,GPIO.OUT)


def forward():
    GPIO.output(ENA,GPIO.HIGH)
    GPIO.output(IN1,GPIO.HIGH)
    GPIO.output(IN2,GPIO.LOW)


def backward():
    GPIO.output(ENA,GPIO.HIGH)
    GPIO.output(IN1,GPIO.LOW)
    GPIO.output(IN2,GPIO.HIGH)

while True:
    forward()
    sleep(1)
    backward()
    sleep(1)
