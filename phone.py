import os
import requests

import sys
import subprocess

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
HORNTIMER = 0

HORN_LIFTED = False

def wave(strip, frame):
	for j in range(strip.numPixels()):
		c = AMP * sin(2*pi*frame + j) + AMP
		color = Color(int(RED*c),int(GREEN*c),int(BLUE*c))
		strip.setPixelColor(j,color)
	strip.show() 

def is_muted():
	process = subprocess.Popen(['amixer -c 1 sget Mic'], shell=True, stdout=subprocess.PIPE )
	output = process.communicate()[0].split("\n")
	is_mute = False

	for line in output:
	    data = line.lower()    
	    if ('mono: capture' in data) and '[off]' in data:
	        is_mute = True  
	return is_mute

def mute():
	subprocess.Popen(['amixer -c 1 sset Mic nocap'], shell=True, stdout=subprocess.PIPE)

def unmute():
	subprocess.Popen(['amixer -c 1 sset Mic cap'], shell=True, stdout=subprocess.PIPE )

if __name__ == '__main__':
	strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
	strip.begin()
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(INPUT_PIN, GPIO.IN)

	while True:
		if FRAME*100 % 1 == 0:
			wave(strip, FRAME)
		FRAME+= 0.0010
		if HORNTIMER > 8000:
			HORN_LIFTED = not GPIO.input(INPUT_PIN)
			muted = is_muted()
			if HORN_LIFTED and muted:
				unmute()
			elif not HORN_LIFTED and not muted:
				mute()
			HORNTIMER = 0
		else:
			HORNTIMER += 1
		if HORN_LIFTED:
			if RINGTIMER == 0:
				requests.get("http://192.168.0.2:4567/?ring")
			RINGTIMER += 1
			if RINGTIMER > 8000:
				RINGTIMER = 0
		if RING and not HORN_LIFTED:
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

		if os.path.exists('ring'):
			RING = True
			TIMER = 0
			os.remove('ring')
