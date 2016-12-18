# -*- coding: utf-8 -*- 
# Bezelie Sample Code for Raspberry Pi
# AquesTalk with Supersonic Distance Sensor

import csv
import time
from time import sleep
from random import randint
import subprocess
import RPi.GPIO as GPIO
import bezelie

csvFile = "bezeTalk.csv"

# Definition
trigger_pin = 18    # GPIO 18
echo_pin = 23       # GPIO 23
short = 10
long = 30

# Set Up
GPIO.setmode(GPIO.BCM)
GPIO.setup(trigger_pin, GPIO.OUT)
GPIO.setup(echo_pin, GPIO.IN)

# Functions
def send_trigger_pulse():
    GPIO.output(trigger_pin, True)
    sleep(0.0001)
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

def talkMessage(trigger):
  data = []
  with open(csvFile, 'rb') as f:  # opening the datafile to read
    for i in csv.reader(f):       
      data.append(i)              # raw data

  data1 = []
  for index,i in enumerate(data): # making a candidate list
    if i[1]==trigger:             # Checking time
      j = int(i[3])*randint(8,12) # Adding random value to probability
      data1.append(i+[j]+[index]) # Candidates data

  maxNum = 0
  for i in data1:                 # decision
    if i[5] > maxNum:             # Whitch is the max probability.
      maxNum = i[5]               # Max probability
      ansNum = i[6]               # Index of answer

  # AquesTalk
  print data[ansNum][2]
  subprocess.call('/home/pi/aquestalkpi/AquesTalkPi -s 120 "'+ data[ansNum ][2] +'" | aplay', shell=True)

# Get Started
bezelie.moveCenter()

# Main Loop
while True:
  d = get_distance()
  print(round(d,1))
  if d < short:
    bezelie.moveHead (20)
    talkMessage("short")
    bezelie.moveHead (0)
  if d >= short and d < long:
    bezelie.moveBack ( 20)
    bezelie.moveBack (-20)
    bezelie.moveBack (  0)
    talkMessage("long")
  else:
    time.sleep(1)

GPIO.cleanup()
