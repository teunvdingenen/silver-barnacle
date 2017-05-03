import RPi.GPIO as GPIO
import time

INPUT_PIN = 21

if __name__ == '__main__':
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(INPUT_PIN, GPIO.OUT)
	GPIO.output(INPUT_PIN, 1)
	# while timeout < 10000:
	#	GPIO.output(INPUT_PIN, 1)
	#	timeout+=1
	#	time.sleep(0.01)
	
	#GPIO.output(INPUT_PIN, 0)
