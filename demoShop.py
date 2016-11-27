# -*- coding: utf-8 -*- 
# Bezelie Special Code for Shanghi-Donya
# 

import csv
import datetime
from time import sleep
from random import randint
import subprocess
import picamera
import RPi.GPIO as GPIO
import bezelie

csvFile = "bezeTalkShop.csv"
openTime = 0
closeTime = 24

# Definition
def timeMessage(timeSlot):
  data = []
  with open(csvFile, 'rb') as f:  # opening the data file to read
    for i in csv.reader(f):       
      data.append(i)              # raw data

  data1 = []
  for index,i in enumerate(data): # making candidate list
    if i[1]==timeSlot:            # Checking time
      j = int(i[3])*randint(1,100)# Adding random to probability
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
bezelie.centering()
subprocess.call('ifconfig | grep inetアドレス.*ブロードキャスト', shell=True)

# Main Loop
try:
  while (True):
    now = datetime.datetime.now()
    print now
    if now.hour >= openTime and now.hour < closeTime: # Activate only in the business hour
      with picamera.PiCamera() as camera:
        camera.resolution = (800, 480)                # Display Resolution
        camera.framerate = 30                         # Frame Rate Max = 30fps
        camera.rotation = 180                         # Up side Down
        camera.led = False
        camera.start_preview()
        sleep (0.2)
      
        pit = 0
        while (True):
          bezelie.moveRot (-5)
          sleep (0.2)
          bezelie.moveYaw (-40, 2)
          sleep (0.5)
          bezelie.moveRot ( 5)
          sleep (0.2)
          bezelie.moveYaw ( 40, 2)
          sleep (1)
          bezelie.moveRot (-5)
          sleep (0.2)
          bezelie.moveYaw ( 0, 2)
          bezelie.moveRot ( 0)
          sleep (0.5)
          bezelie.movePit (-15)
          sleep (0.2)
          bezelie.moveRot ( 10)
          sleep (0.2)
          bezelie.moveRot (-10)
          sleep (0.4)
          bezelie.moveRot ( 0)
          timeMessage("afternoon")
          sleep (0.5)
          pit += 5
          if pit > 10:
            pit = -15
          bezelie.movePit (pit)
          sleep (0.2)
    else:
      print "営業時間外です"
      sleep(60)

except:
  subprocess.call('ifconfig | grep inetアドレス.*ブロードキャスト', shell=True)
