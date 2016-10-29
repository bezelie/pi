# -*- coding:utf-8 -*-
# Bezelie Sample Code for Raspberry Pi : Distance Game

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

    answer = randint(0,1)
    if answer == 0:
      bezelie.movePit (-20)
      print ("後ろ！")
      if randint(0,1) == 0:
        subprocess.call('/home/pi/aquestalkpi/AquesTalkPi -s 120 "後ろ！" | aplay', shell=True)
      else:
        subprocess.call('/home/pi/aquestalkpi/AquesTalkPi -s 120 "前の逆！" | aplay', shell=True)
    else:
      bezelie.movePit (20)
      print ("前！")
      if randint(0,1) == 0:
        subprocess.call('/home/pi/aquestalkpi/AquesTalkPi -s 120 "前！" | aplay', shell=True)
      else:
        subprocess.call('/home/pi/aquestalkpi/AquesTalkPi -s 120 "後ろの逆！" | aplay', shell=True)
    time.sleep (3.5 - score * 1)

    while True:
      dist = round(get_distance(),1)
      if dist > 10 and < 300:
        break

    bezelie.movePit (0)
    if answer == 0:
      if dist > 120:
        score += 1
        bezelie.moveRot (-20)
        time.sleep (0.5)
        bezelie.moveRot (20)
        time.sleep (0.5)
        bezelie.moveRot (0)
        print ("巧い！")
        subprocess.call('/home/pi/aquestalkpi/AquesTalkPi -s 120 "巧い！" | aplay', shell=True)
        time.sleep (0.5)
        if score > 3:
          mode = 1
      else:
        mode = 2
        print ("近すぎー")
        subprocess.call('/home/pi/aquestalkpi/AquesTalkPi -s 120 "近すぎー" | aplay', shell=True)
        time.sleep (0.5)
    else:
      if dist < 80:
        score += 1
        bezelie.moveRot (-20)
        time.sleep (0.5)
        bezelie.moveRot (20)
        time.sleep (0.5)
        bezelie.moveRot (0)
        print ("イイね！")
        subprocess.call('/home/pi/aquestalkpi/AquesTalkPi -s 120 "イイね！" | aplay', shell=True)
        time.sleep (0.5)
        if score > 3:
          mode = 1
      else:
        mode = 2
        print ("遠いよー")
        subprocess.call('/home/pi/aquestalkpi/AquesTalkPi -s 120 "遠いよー" | aplay', shell=True)
        time.sleep (0.5)
  if mode == 1:
    print ("凄いっクリアーだよ")
    subprocess.call('/home/pi/aquestalkpi/AquesTalkPi -s 120 "クリアーだよー" | aplay', shell=True)
    print ("おめでとー")
    subprocess.call('/home/pi/aquestalkpi/AquesTalkPi -s 120 "おめでとー" | aplay', shell=True)
  else:
    bezelie.movePit (20)
    print ("鈍いねー")
    subprocess.call('/home/pi/aquestalkpi/AquesTalkPi -s 120 "ちょっと鈍いね" | aplay', shell=True)
    time.sleep (0.5)
    bezelie.moveRot (-20)
    time.sleep (0.5)
    bezelie.moveRot (20)
    time.sleep (0.5)
    print ("ゲームオーバー")
    subprocess.call('/home/pi/aquestalkpi/AquesTalkPi -s 120 "ゲームオーバー" | aplay', shell=True)
    bezelie.moveRot (0)
    bezelie.movePit (0)
    time.sleep (0.5)
except KeyboardInterrupt:
  print " Interrupted by Keyboard"

GPIO.cleanup()
