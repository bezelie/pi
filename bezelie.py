# -*- coding: utf-8 -*-
# Bezelie Python Module for Raspberry Pi
import RPi.GPIO as GPIO
from time import sleep
import smbus
import math

bus = smbus.SMBus(1)
address_pca9685 = 0x40 # When you connect other I2C devices, you may have to change this number.

# Constants
dutyMax = 490     #
dutyMin = 110     #
dutyCenter = 300  #
steps = 1         #

# Global Valiables
headNow = backNow = stageNow = dutyCenter

# Functions
def initPCA9685():
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
  adj = 0       # Head servo adjustment
  max = 360     # Downward limit
  min = 280     # Upward limit
  global headNow
  headNow = moveServo (2, degree, adj, max, min, speed, headNow)

def moveBack (degree, speed=1):
  adj = 0       # Back servo adjustment
  max = 380     # AntiClockwise limit
  min = 220     # Clockwise limit
  global backNow
  backNow = moveServo (1, degree, adj, max, min, speed, backNow)

def moveStage (degree, speed=1):
  adj = 0      # Stage servo adjustment
  max = 390    # AntiClockWise limit
  min = 210    # Clocwise limit
  global stageNow
  stageNow = moveServo (0, degree, adj, max, min, speed,stageNow)

def moveCenter ():
    moveHead (0)
    moveBack (0)
    moveStage (0)

# Centering Servo Motors
try:
    moveHead (20)
    moveHead (-20)
    moveHead (0)
    moveBack (20)
    moveBack (-20)
    moveBack (0)
    moveStage (20)
    moveStage (-20)
    moveStage (0)
except KeyboardInterrupt:
  print " Interrupted by Keyboard"
