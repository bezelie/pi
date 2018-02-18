# Bezelie Sample Code for Raspberry Pi : Colur LED Blink Test

import RPi.GPIO as GPIO
from time import sleep

# Definition
ledRed = 16       # as Red
ledBlue = 20      # as Blue
ledGreen = 21     # as Green
interval = 0.1

# Set Up
GPIO.setmode(GPIO.BCM)
GPIO.setup(ledRed, GPIO.OUT)
GPIO.setup(ledBlue, GPIO.OUT)
GPIO.setup(ledGreen, GPIO.OUT)

# Functions
def ledOff():
  GPIO.output (ledRed, False)
  GPIO.output (ledBlue, False)
  GPIO.output (ledGreen, False)
  sleep(0.04)

# Main Loop
try:
  while True:
    GPIO.output (ledRed, True)
    sleep(interval)
    ledOff()
    GPIO.output (ledBlue, True)
    sleep(interval)
    ledOff()
    GPIO.output (ledGreen, True)
    sleep(interval)
    ledOff()
    GPIO.output (ledRed, True)
    GPIO.output (ledBlue, True)
    sleep(interval)
    ledOff()
    GPIO.output (ledBlue, True)
    GPIO.output (ledGreen, True)
    sleep(interval)
    ledOff()
    GPIO.output (ledGreen, True)
    GPIO.output (ledRed, True)
    sleep(interval)
    ledOff()
    GPIO.output (ledRed, True)
    GPIO.output (ledBlue, True)
    GPIO.output (ledGreen, True)
    sleep(interval)
    ledOff()

except KeyboardInterrupt:
  print " Interrupted by Keyboard"

GPIO.cleanup()
