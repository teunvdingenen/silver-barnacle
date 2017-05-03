import os
import requests

import time
import RPi.GPIO as GPIO
from math import *
from neopixel import *

INPUT_PIN = 23

if __name__ == '__main__':
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(INPUT_PIN, GPIO.OUT)
	timeout = 0
	while timeout < 10000:
		GPIO.output(INPUT_PIN, 1)
		timeout+=1
	
	GPIO.output(INPUT_PIN, 0)
