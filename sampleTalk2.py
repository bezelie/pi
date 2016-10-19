# -*- coding: utf-8 -*- Bezelie Sample Code for Raspberry Pi selecting 
# messages from csv file

import csv
import datetime
from time import sleep
from random import randint
import subprocess
import bezelie

csvFile = "bezeTalk.csv"

# Definition
def timeMessage(timeSlot):
  data = []
  with open(csvFile, 'rb') as f:  # open file
    for i in csv.reader(f):       #
      data.append(i)              #

  data1 = []
  for index,i in enumerate(data): #
    if i[1]==timeSlot:            #
      j = int(i[3])/(int(i[4])+randint(1,2))
      data1.append(i+[j]+[index])

  maxNum = 0
  for i in data1:
    if i[5] > maxNum:
      maxNum = i[5]
      ansNum = i[6]

  data[ansNum][4] = int(data[ansNum][4])+1

  with open(csvFile, 'wb') as f:
    csv.writer(f).writerows(data)

  print data[ansNum][2]
  subprocess.call('/home/pi/aquestalkpi/AquesTalkPi -s 120 "'+ data[ansNum][2] +'" | aplay&', shell=True)
  bezelie.movePit (20, 1)
  sleep(2)
  bezelie.movePit (0, 1)
  sleep(2)

# Get Started
bezelie.centering()

# Main Loop
try:
  while (True):
    now = datetime.datetime.now()
    if now.hour < 8:                # mid night
      pass
#      sleep(60)
    elif now.hour == 8:
      timeMessage("awaking")
#      sleep(randint(60*20,60*40))
    elif now.hour < 12:
      timeMessage("morning")
#      sleep(randint(60*50,60*70))
    elif now.hour == 12:
      timeMessage("noon")
#      sleep(randint(60*20,60*40))
    elif now.hour < 16:
      timeMessage("afternoon")
#      sleep(randint(60*110,60*130))
    elif now.hour < 19:
      timeMessage("evening")
#      sleep(randint(60*50,60*70))
    elif now.hour < 23:
      timeMessage("night")
#      sleep(randint(60*50,60*70))
    else:
      timeMessage("bedtime")
#      sleep(randint(60*20,60*40))
    sleep(1)

except KeyboardInterrupt:
  print " Interrupted by Keyboard"
