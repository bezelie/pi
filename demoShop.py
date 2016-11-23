# -*- coding: utf-8 -*- 
# Bezelie Special Code for Shanghi-Donya
# 

import csv
import datetime
from time import sleep
from random import randint
import subprocess
import picamera
import bezelie

csvFile = "bezeTalkShop.csv"
openTime = 11
closeTime = 20

# Definition
def timeMessage(timeSlot):
  data = []
  with open(csvFile, 'rb') as f:  # opening the file to read
    for i in csv.reader(f):       
      data.append(i)              

  data1 = []
  for index,i in enumerate(data): # making candidate list
    if i[1]==timeSlot:            
      j = int(i[3])*randint(1,100) # Calucurate Probability
      data1.append(i+[j]+[index])

  maxNum = 0
  for i in data1:                 # decision
    if i[5] > maxNum:             # Whitch is the max.
      maxNum = i[5]               # Probability
      ansNum = i[6]               # index

  # AquesTalk
  print data[ansNum ][2]
  subprocess.call('/home/pi/aquestalkpi/AquesTalkPi -s 120 "'+ data[ansNum ][2] +'" | aplay', shell=True)

# Get Started
bezelie.centering()

# Main Loop
try:
  while (True):
    now = datetime.datetime.now()
    print now
    if now.hour >= openTime and now.hour <= closeTime:
      with picamera.PiCamera() as camera:
        camera.resolution = (800, 480)
        camera.framerate = 30              # Max = 30
        camera.rotation = 180
        camera.start_preview()
        sleep (0.2)
      
        pit = 0
        while (True):
          bezelie.moveRot (-5)
          sleep (0.2)
          bezelie.moveYaw (-40, 2)
          sleep (1)
          bezelie.moveRot ( 5)
          sleep (0.2)
          bezelie.moveYaw ( 40, 2)
          sleep (1.5)
          bezelie.moveRot (-5)
          sleep (0.2)
          bezelie.moveYaw ( 0, 2)
          sleep (1)
          bezelie.moveRot ( 0)
          sleep (0.2)
          pit += 5
          if pit > 10:
            pit = -15
          bezelie.movePit (pit)
          timeMessage("afternoon")
          sleep (1)
    else:
      sleep(60 )

except KeyboardInterrupt:
  print " Interrupted by Keyboard"
