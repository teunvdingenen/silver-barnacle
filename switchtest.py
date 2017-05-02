import os
import requests

import time
import RPi.GPIO as GPIO
from math import *
from neopixel import *

INPUT_PIN = 27

if __name__ == '__main__':
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(INPUT_PIN, GPIO.IN)
	timeout = 0
	while timeout < 10000:
		if GPIO.input(INPUT_PIN):
			print "ON"
		else:
			print "OFF"
		timeout+=1
