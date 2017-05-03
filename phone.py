import os
import requests

import sys
import subprocess

import time
import RPi.GPIO as GPIO

INPUT_PIN = 27
OUTPUT_PIN = 23

RING = False
TIMER = 0

RINGTIMER = 0

def mute():
	subprocess.Popen(['amixer -c 1 sset Mic nocap'], shell=True, stdout=subprocess.PIPE)

def unmute():
	subprocess.Popen(['amixer -c 1 sset Mic cap'], shell=True, stdout=subprocess.PIPE )

if __name__ == '__main__':
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(INPUT_PIN, GPIO.IN)
	GPIO.setup(OUTPUT_PIN, GPIO.OUT)
	GPIO.output(OUTPUT_PIN, False)	

	while True:
		HORN_LIFTED = not GPIO.input(INPUT_PIN)
		if HORN_LIFTED:
			unmute()
		else:
			mute()
		if HORN_LIFTED:
			if RINGTIMER == 0:
				try:
					r = requests.get("http://192.168.0.2:4567/?ring")
				except requests.exceptions.RequestException as e:
					m = 0 # do nothing
			RINGTIMER += 1
			if RINGTIMER > 6:
				RINGTIMER = 0
		if TIMER > 6:
			TIMER = 0
			RING = False
		else:
			TIMER += 1

		if os.path.exists('ring'):
			RING = True
			TIMER = 0
			os.remove('ring')
		time.sleep(0.5)
