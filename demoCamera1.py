# -*- coding: utf-8 -*-
# Bezelie demo Code for Raspberry Pi : Camera and Range Sensor

import RPi.GPIO as GPIO
import time
import picamera
import subprocess
import bezelie

# Settin Up
trigger_pin = 18    # GPIO 18
echo_pin = 23       # GPIO 23
actionDistance = 10 # centi mater
GPIO.setmode(GPIO.BCM)
GPIO.setup(trigger_pin, GPIO.OUT)
GPIO.setup(echo_pin, GPIO.IN)
photoNo = 1         # jpg File Number

# Function
def send_trigger_pulse():
    GPIO.output(trigger_pin, True)
    time.sleep(0.0001)
    GPIO.output(trigger_pin, False)

def wait_for_echo(value, timeout):
    count = timeout
    while GPIO.input(echo_pin) != value and count > 0:
        count -= 1

def get_distance():
    send_trigger_pulse()
    wait_for_echo(True, 10000)
    start = time.time()
    wait_for_echo(False, 10000)
    finish = time.time()
    pulse_len = finish - start
    distance  = pulse_len / 0.000058
    return (distance)

def sensorCheck():
    global photoNo
    if get_distance() < actionDistance:
      bezelie.centering()
      subprocess.call('/home/pi/aquestalkpi/AquesTalkPi -s 120 "こんにちわー" | aplay', shell=True)
      camera.stop_preview()
      camera.capture('/home/pi/Pictures/image'+ str(photoNo) +'.jpg')
      photoNo += 1
#      camera.capture_continuous('image{counter}.jpg')
      camera.start_preview()
      time.sleep(0.5)

# Centering All Servos
bezelie.centering()

# Main Loop
try:
  with picamera.PiCamera() as camera:
    camera.resolution = (800, 480)   # Change this number for your display
    camera.rotation = 180            # comment out if your screen upside down
    camera.start_preview()
    time.sleep(0.2)
    pit = 0
    while (True):
      bezelie.moveRot (-15)
      bezelie.moveYaw (-40, 2)
      sensorCheck()
      time.sleep (1)
      bezelie.moveRot (15)
      bezelie.moveYaw (40, 2)
      sensorCheck()
      time.sleep (1)
      pit += 10
      if pit > 10:
        pit = -20
      bezelie.movePit (pit)
      time.sleep (1)

except KeyboardInterrupt:
  print " Interrupted by Keyboard"

GPIO.cleanup()
