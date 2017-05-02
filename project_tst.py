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

INPUT_PIN = 27

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
	while True:
		for j in range(0, strip.numPixels()):
			color = Color(RED,GREEN,BLUE)
			strip.setPixelColor(j,color)
		strip.show()
