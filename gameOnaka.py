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
  subprocess.call('/home/pi/aquestalkpi/AquesTalkPi -s 120 "さぁ、お腹大砲、始めるよー" | aplay', shell=True)
  time.sleep(1)
  subprocess.call('/home/pi/aquestalkpi/AquesTalkPi -s 120 "お腹で風を起こそう！" | aplay', shell=True)
  bezelie.moveRot (0)
  time.sleep(1)
  mode = 0
  score = 0
  while mode == 0:
    print ("僕から１メートル離れてね")
    subprocess.call('/home/pi/aquestalkpi/AquesTalkPi -s 120 "僕から１メートル離れてね" | aplay', shell=True)
    time.sleep(0.5)
    while True:
      dist = round(get_distance(),1)
      if dist > 90 and dist < 110:
        break
    print ("オッケー")
    subprocess.call('/home/pi/aquestalkpi/AquesTalkPi -s 120 "オッケー" | aplay', shell=True)
    time.sleep(0.5)

    print ("おなかを引っ込めてー")
    subprocess.call('/home/pi/aquestalkpi/AquesTalkPi -s 120 "おなかを引っ込めてー" | aplay', shell=True)
    time.sleep(0.5)

    while True:
      distB = round(get_distance(),1)
      if distB > 100 and distB < 300:
        break

    print ("３")
    subprocess.call('/home/pi/aquestalkpi/AquesTalkPi -s 120 "３" | aplay', shell=True)
    time.sleep(0.2)
    print ("２")
    subprocess.call('/home/pi/aquestalkpi/AquesTalkPi -s 120 "２" | aplay', shell=True)
    time.sleep(0.2)
    print ("１")
    subprocess.call('/home/pi/aquestalkpi/AquesTalkPi -s 120 "１" | aplay', shell=True)

    while True:          # flying check
      dist = round(get_distance(),1)
      if dist > 10 and dist < 400:
        break

    if dist < 80:       # flying
#      mode = 2
      print ("フライングだよー")
      subprocess.call('/home/pi/aquestalkpi/AquesTalkPi -s 120 "フライングー" | aplay', shell=True)
      time.sleep(1)
      continue

    time.sleep(0.1)

    while True:
      distA = round(get_distance(),1)
      if distA > 10 and distA < 200:
        break

    bezelie.movePit (-20)
    i = distB - distA
    print i
    subprocess.call('/home/pi/aquestalkpi/AquesTalkPi -s 120 "記録" | aplay', shell=True)
#    time.sleep(0.5)
    subprocess.call('/home/pi/aquestalkpi/AquesTalkPi -s 120 "'+ str(i) +'" | aplay', shell=True)
#    time.sleep(0.5)
    subprocess.call('/home/pi/aquestalkpi/AquesTalkPi -s 120 "メートル" | aplay', shell=True)
    time.sleep(0.5)
    if i < 10:
      print ("失敗でーす")
      subprocess.call('/home/pi/aquestalkpi/AquesTalkPi -s 120 "あなた、駄目な人ですね" | aplay', shell=True)
      time.sleep(1)
    elif i < 20:
      print ("まぁまぁかな")
      subprocess.call('/home/pi/aquestalkpi/AquesTalkPi -s 120 "ふつーだね" | aplay', shell=True)
      time.sleep(1)
    elif i < 30:
      print ("なかなかグッド")
      subprocess.call('/home/pi/aquestalkpi/AquesTalkPi -s 120 "ぐっじょぶ" | aplay', shell=True)
      time.sleep(1)
    else:
      print ("どっひゃー")
      subprocess.call('/home/pi/aquestalkpi/AquesTalkPi -s 120 "どっひゃーっ！" | aplay', shell=True)
      bezelie.moveRot (-20)
      time.sleep (0.5)
      bezelie.moveRot (20)
      time.sleep (0.5)
      bezelie.moveRot (0)
      print ("チャンピオン")
      subprocess.call('/home/pi/aquestalkpi/AquesTalkPi -s 120 "ゆーあー、ちゃんぴおーん" | aplay', shell=True)
      time.sleep(1)
    mode = 1
    time.sleep (0.5)
except KeyboardInterrupt:
  print " Interrupted by Keyboard"

GPIO.cleanup()
