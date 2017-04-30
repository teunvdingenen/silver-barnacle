import os
import requests

import time
import RPi.GPIO as GPIO
from math import *
from neopixel import *

# LED strip configuration:
LED_COUNT      = 24      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

INPUT_PIN = 17

RED 		= 255
GREEN		= 165
BLUE		= 0

FRAME = 0
AMP = 0

RING = False
TIMER = 0

RINGTIMER = 0

def wave(strip, frame):
	for j in range(0, strip.numPixels()):
		c = AMP * sin(2*pi*frame + j) + AMP
		color = Color(int(RED*c),int(GREEN*c),int(BLUE*c))
		strip.setPixelColor(j,color)
	strip.show() 

if __name__ == '__main__':
	strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
	strip.begin()
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(INPUT_PIN, GPIO.IN)

	while True:
		FRAME+= 0.0008
		if GPIO.input(INPUT_PIN):
			if RINGTIMER == 0:
				requests.get("http://localhost:4567/?ring")
			RINGTIMER += 1
			if RINGTIMER > 8000:
				RINGTIMER = 0
		if RING:
			AMP += 0.00005		
			TIMER += 1
		else:
			AMP -= 0.0001
		if AMP > 0.5:
			AMP = 0.5
		elif AMP < 0:
			AMP = 0

		if FRAME % 1 == 0:
			FRAME = 0

		if TIMER > 5000:
			TIMER = 0
			RING = False

		wave(strip, FRAME)
		if os.path.exists('ring'):
			RING = True
			TIMER = 0
			os.remove('ring')
