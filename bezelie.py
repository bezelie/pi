#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Bezelie Python Module for Raspberry Pi

import RPi.GPIO as GPIO
from time import sleep
import smbus  # I2C module
import math
import bezeConfig

bus = smbus.SMBus(1) # I2C
address_pca9685 = 0x40 # When you connect other I2C devices, you may have to change this number.

# Read bezeConfig.py
headAdj = bezeConfig.headAdj
backAdj = bezeConfig.backAdj
stageAdj = bezeConfig.stageAdj

# Constants
dutyMax = 490     #
dutyMin = 110     #
dutyCenter = 300  #
steps = 1         #

# Global Valiables
headNow = backNow = stageNow = dutyCenter

# Functions
def initPCA9685():
  try:
    bus.write_byte_data(address_pca9685, 0x00, 0x00)
    freq = 0.9*50
    prescaleval = 25000000.0    # 25MHz
    prescaleval /= 4096.0       # 12-bit
    prescaleval /= float(freq)
    prescaleval -= 1.0
    prescale = int(math.floor(prescaleval + 0.5))
    oldmode = bus.read_byte_data(address_pca9685, 0x00)
    newmode = (oldmode & 0x7F) | 0x10             
    bus.write_byte_data(address_pca9685, 0x00, newmode) 
    bus.write_byte_data(address_pca9685, 0xFE, prescale) 
    bus.write_byte_data(address_pca9685, 0x00, oldmode)
    sleep(0.005)
    bus.write_byte_data(address_pca9685, 0x00, oldmode | 0xa1)
  except:
    print "ERROR:サーボドライバボードがI2Cにつながっていないようですね"

def setPCA9685Duty(channel, on, off):
  channelpos = 0x6 + 4*channel
  try:
    bus.write_i2c_block_data(address_pca9685, channelpos, [on&0xFF, on>>8, off&0xFF, off>>8] )
  except IOError:
    pass

def moveServo (id, degree, adj, max, min, speed, now):
  dst = (dutyMin-dutyMax)*(degree+adj+90)/180 + dutyMax
  if speed == 0:
    setPCA9685Duty(id, 0, dst)
    sleep(0.001 * math.fabs(dst-now))
    now = dst    
  if dst > max: dst = max
  if dst < min: dst = min
  while (now != dst):
    if now < dst:
      now += steps
      if now > dst: now = dst
    else:
      now -= steps
      if now < dst: now = dst
    setPCA9685Duty(id, 0, now)
    sleep(0.004 * steps *(speed))
  return (now)

def moveHead (degree, speed=1):
  global headAdj
  max = 360     # Downward limit
  min = 230     # Upward limit
  global headNow
  headNow = moveServo (2, degree, headAdj, max, min, speed, headNow)

def moveBack (degree, speed=1):
  global backAdj
  max = 380     # AntiClockwise limit
  min = 220     # Clockwise limit
  global backNow
  backNow = moveServo (1, degree, backAdj, max, min, speed, backNow)

def moveStage (degree, speed=1):
  global stageAdj
  max = 390    # AntiClockWise limit
  min = 210    # Clocwise limit
  global stageNow
  stageNow = moveServo (0, degree, stageAdj, max, min, speed,stageNow)

def moveCenter ():
  moveHead (headAdj)
  moveBack (backAdj)
  moveStage (stageAdj)

# BezeActions
# actHappyS(), actHappy(), actHappyB()
# actTalk(),actYes(),actSad(),actAlarm(),actWhy(),actSleep()

def actHappyS (time=1):
  moveHead (10)
  moveBack (10)
  moveBack (-10)
  moveBack (10)
  moveBack (-10)
  moveBack (0)
  sleep (time)
  moveHead (0)

def actHappy (time=1):
  moveHead (20)
  moveBack (10)
  moveBack (-10)
  moveBack (10)
  moveBack (-10)
  moveBack (0)
  sleep (time)
  moveHead (0)

def actHappyB (time=1):
  moveHead (20)
  moveBack (20)
  moveBack (-20)
  moveBack (20)
  moveBack (-20)
  moveBack (0)
  sleep (time)
  moveHead (0)

def actTalk (time=1):
  moveHead (-10)
  moveHead (0)
  moveHead (-10)
  moveHead (0)

def actYes (time=1):
  moveHead (-20)
  moveHead (0)

def actSad (time=1):
  moveHead (-20)
  moveBack (10, 4)
  moveBack (-10,4)
  moveBack (0,4)
  sleep (time)
  moveHead (0)

def actAlarm (time=1):
  moveHead (20)
  moveStage (40)
  moveStage (-40)
  moveStage (40)
  moveStage (-40)
  moveStage (0)
  sleep (time)
  moveHead (0)

def actWhy (time=1):
  moveBack (30)
  sleep (time)
  moveBack (0, 2)

def actSleep (time=1):
  moveHead (-20, 5)
  moveHead (-15, 5)
  moveHead (-20 ,5)
  moveHead (-15, 5)
  moveHead (-20 ,5)
  sleep (time)
  moveHead (0)

# Centering Servo Motors
if __name__ == "__main__":  # Do only when this is done as a script
  moveHead (20)
  moveHead (-20)
  moveHead (headAdj)
  moveBack (20)
  moveBack (-20)
  moveBack (backAdj)
  moveStage (20)
  moveStage (-20)
  moveStage (stageAdj)
