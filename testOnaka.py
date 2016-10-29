# -*- coding:utf-8 -*-
# Bezelie Sample Code for Raspberry Pi : onaka Game

import RPi.GPIO as GPIO
import time
import subprocess
import bezelie
from random import randint

# Definition
trigger_pin = 18    # GPIO 18
echo_pin = 23       # GPIO 23
actionDistance = 10 # centi mater
GPIO.setmode(GPIO.BCM)
GPIO.setup(trigger_pin, GPIO.OUT)
GPIO.setup(echo_pin, GPIO.IN)

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

# Main Loop
try:
  bezelie.centering()
  time.sleep (1)
  bezelie.moveRot (-20)
  time.sleep(0.5)
  bezelie.moveRot (20)
  print ("さぁ、始めるよー")
  subprocess.call('/home/pi/aquestalkpi/AquesTalkPi -s 120 "さぁ、始めるよー" | aplay', shell=True)
  bezelie.moveRot (0)
  time.sleep(2)
  mode = 0
  score = 0
  while mode == 0:
    print ("僕から１メートル離れてね")
    subprocess.call('/home/pi/aquestalkpi/AquesTalkPi -s 120 "僕から１メートル離れてね" | aplay', shell=True)
    time.sleep(1)
    while True:
      dist = round(get_distance(),1)
      if dist > 80 and dist < 120:
        break
    print ("オッケー")
    subprocess.call('/home/pi/aquestalkpi/AquesTalkPi -s 120 "オッケー" | aplay', shell=True)
    time.sleep(1)

    print ("おなかを引っ込めてー")
    subprocess.call('/home/pi/aquestalkpi/AquesTalkPi -s 120 "おなかを引っ込めてー" | aplay', shell=True)
    time.sleep(1)
    while True:
      distB = round(get_distance(),1)
      if distB > 100 and distB < 200:
        break

    print ("３")
    subprocess.call('/home/pi/aquestalkpi/AquesTalkPi -s 120 "３" | aplay', shell=True)
    time.sleep(0.5)
    print ("２")
    subprocess.call('/home/pi/aquestalkpi/AquesTalkPi -s 120 "２" | aplay', shell=True)
    time.sleep(0.5)
    print ("１")
    subprocess.call('/home/pi/aquestalkpi/AquesTalkPi -s 120 "１" | aplay', shell=True)
    time.sleep(0.5)

    while True:
      distA = round(get_distance(),1)
      if distA > 10 and distA < 100:
        break

    bezelie.movePit (-20)
    i = distB - distA
    if i < 10:
      subprocess.call('/home/pi/aquestalkpi/AquesTalkPi -s 120 "あなた、駄目な人ですね" | aplay', shell=True)
      time.sleep(1)
    elif i < 20:
      subprocess.call('/home/pi/aquestalkpi/AquesTalkPi -s 120 "ふつーだね" | aplay', shell=True)
      time.sleep(1)
    elif i < 40:
      subprocess.call('/home/pi/aquestalkpi/AquesTalkPi -s 120 "ぐっじょぶ" | aplay', shell=True)
      time.sleep(1)
    else:
        bezelie.moveRot (-20)
        time.sleep (0.5)
        bezelie.moveRot (20)
        time.sleep (0.5)
        bezelie.moveRot (0)
        print ("巧い！")
      subprocess.call('/home/pi/aquestalkpi/AquesTalkPi -s 120 "ちゃんぴおーん" | aplay', shell=True)
      time.sleep(1)
　　mode = 1
    time.sleep (0.5)
except KeyboardInterrupt:
  print " Interrupted by Keyboard"

GPIO.cleanup()
