# Bezelie Sample Code for Raspberry Pi : LED test

import RPi.GPIO as GPIO
from time import sleep

# Definition
led_pin = 24       # GPIO 24

# Set Up
GPIO.setmode(GPIO.BCM)
GPIO.setup(led_pin, GPIO.OUT)

# Main Loop
try:
  while True:
    GPIO.output (led_pin, True)
    sleep(0.5)
    GPIO.output (led_pin, False)
    sleep(0.5)
except KeyboardInterrupt:
  print " Interrupted by Keyboard"

GPIO.cleanup()
