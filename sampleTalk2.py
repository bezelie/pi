# -*- coding: utf-8 -*- Bezelie Sample Code for Raspberry Pi selecting 
# speaking messages referring to csv file

import csv
import datetime
from time import sleep
from random import randint
import subprocess
import bezelie

csvFile = "bezeTalk.csv"
awakingTime = 7
sleepingTime = 24

# Definition
def timeMessage(timeSlot):
  data = []
  with open(csvFile, 'rb') as f:  # opening the file to read
    for i in csv.reader(f):       
      data.append(i)              

  data1 = []
  for index,i in enumerate(data): # making candidate list
    if i[1]==timeSlot:            
      j = int(i[3])*randint(9,11)
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
  bezelie.movePit (-20, 1)
  subprocess.call('/home/pi/aquestalkpi/AquesTalkPi -s 120 "'+ data[ansNum][2] +'" | aplay', shell=True)
  sleep(0.5)
  bezelie.movePit (0, 1)
  sleep(2)

# Get Started
bezelie.centering()

# Main Loop
try:
  while (True):
    now = datetime.datetime.now()
    print now
    if now.hour < awakingTime:
      print "It is a midnight"
      sleep(60)
    elif now.hour == awakingTime:
      print "It is an awaking time"
      timeMessage("awaking")
      sleep(randint(60*10,60*20))
    elif now.hour < 12:
      print "It is a morning"
      timeMessage("morning")
      sleep(randint(60*50,60*70))
    elif now.hour == 12:
      print "It is about noon"
      timeMessage("noon")
      sleep(randint(60*20,60*40))
    elif now.hour < 16:
      print "It is an afternoon"
      timeMessage("afternoon")
      sleep(randint(60*110,60*130))
    elif now.hour < 19:
      print "It is an evening"
      timeMessage("evening")
      sleep(randint(60*50,60*70))
    elif now.hour < sleepingTime-1:
      print "It is a night"
      timeMessage("night")
      sleep(randint(60*50,60*70))
    else:
      print "It is a time to go to the bed"
      timeMessage("bedtime")
      sleep(randint(60*20,60*40))

except KeyboardInterrupt:
  print " Interrupted by Keyboard"
