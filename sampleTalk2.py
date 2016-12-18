# -*- coding: utf-8 -*-
# Bezelie Sample Code for Raspberry Pi
# speaking random messages referring to csv file

import csv
import datetime
from time import sleep
from random import randint
import subprocess
import bezelie

csvFile = "bezeTalk.csv"
awakingTime = 7
sleepingTime = 24
interval = 0.1                    # seconds between the talks

# Functions
def talkMessage(trigger):
  data = []
  with open(csvFile, 'rb') as f:  # opening the file to read
    for i in csv.reader(f):       
      data.append(i)              

  data1 = []
  for index,i in enumerate(data): # making candidate list
    if i[1]==trigger:            
      j = int(i[3])*randint(1,10)
      data1.append(i+[j]+[index])

  maxNum = 0
  for i in data1:                 # decision
    if i[5] > maxNum:
      maxNum = i[5]
      ansNum = i[6]

  data[ansNum][4] = int(data[ansNum][4])+1 # adding counter

  with open(csvFile, 'wb') as f:  # opening the file to overwrite
    csv.writer(f).writerows(data)

  # AquesTalk
  print data[ansNum][2]
  bezelie.moveHead (20)
  subprocess.call('/home/pi/aquestalkpi/AquesTalkPi -s 120 "'+ data[ansNum][2] +'" | aplay', shell=True)
  sleep(0.5)
  bezelie.moveHead (0, 2)

# Get Started
bezelie.initPCA9685()
bezelie.moveCenter()

# Main Loop
try:
  while (True):
    now = datetime.datetime.now()
    print now
    if now.hour < awakingTime:
      print "It is a midnight"
      sleep(interval)
    elif now.hour == awakingTime:
      print "It is an awaking time"
      talkMessage("awaking")
      sleep(interval * randint(10,20))
    elif now.hour < 12:
      print "It is a morning"
      talkMessage("morning")
      sleep(interval * randint(50,70))
    elif now.hour == 12:
      print "It is about noon"
      talkMessage("noon")
      sleep(interval * randint(20,40))
    elif now.hour < 16:
      print "It is an afternoon"
      talkMessage("afternoon")
      sleep(interval * randint(110,130))
    elif now.hour < 19:
      print "It is an evening"
      talkMessage("evening")
      sleep(interval * randint(50,70))
    elif now.hour < sleepingTime-1:
      print "It is a night"
      talkMessage("night")
      sleep(interval * randint(50,70))
    else:
      print "It is a time to go to the bed"
      talkMessage("bedtime")
      sleep(interval * randint(20,40))

except KeyboardInterrupt:
  print " Interrupted by Keyboard"
