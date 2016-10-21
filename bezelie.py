# Bezelie python module for Raspberry Pi

from Adafruit_PWM_Servo_Driver import PWM
from  time import sleep

pwm = PWM(0x40)

# Constants
pulseMax = 520 #
pulseMin = 100 #
pulseMid = pulseMin + (pulseMax - pulseMin)/2 # center of pulse
pitAdj = 0     # pitch adjustment
rotAdj = 0     # rotation adjustment
yawAdj = 0     # yaw adjustment
pitMin = -30   # Upward
pitMax =  30   # Downward
rotMin = -30   # Clockwise
rotMax =  30   # AntiClockwise
yawMin = -40   # Clocwise
yawMax =  40   # AntiClockWise
pwm.setPWMFreq(47)   # Set frequency to 50 Hz
servoStep = 5
defaultSpeed = 0

# Global Valiables
pitNow = rotNow = yawNow = pulseMid

# Functions
def movePit (pit, speed=defaultSpeed):
  global pitNow
  if pit > pitMax:
    pit = pitMax
  if pit < pitMin:
    pit = pitMin
  pitDest = int( float(pit + 90)/180 * (pulseMax - pulseMin) + pulseMin)
  while (pitNow != pitDest):
    if pitNow < pitDest:
      pitNow += servoStep
      if pitNow > pitDest:
        pitNow = pitDest
    if pitNow > pitDest:
      pitNow -= servoStep
      if pitNow < pitDest:
        pitNow = pitDest
    pwm.setPWM(2, 0, pitNow + pitAdj)
    sleep (speed * 0.01)

def moveRot (rot, speed=defaultSpeed):
  global rotNow
  if rot > rotMax:
    rot = rotMax
  if rot < rotMin:
    rot = rotMin
  rotDest = int( float(rot + 90)/180 * (pulseMax - pulseMin) + pulseMin)
  while (rotNow != rotDest):
    if rotNow < rotDest:
      rotNow += servoStep
      if rotNow > rotDest:
        rotNow = rotDest
    if rotNow > rotDest:
      rotNow -= servoStep
      if rotNow < rotDest:
        rotNow = rotDest
    pwm.setPWM(1, 0, rotNow + rotAdj)
    sleep (speed * 0.01)

def moveYaw (yaw, speed=defaultSpeed):
  global yawNow
  if yaw > yawMax:
    yaw = yawMax
  if yaw < yawMin:
    yaw = yawMin
  yawDest = int( float(yaw + 90)/180 * (pulseMax - pulseMin) + pulseMin)
  while (yawNow != yawDest):
    if yawNow < yawDest:
      yawNow += servoStep
      if yawNow > yawDest:
        yawNow = yawDest
    if yawNow > yawDest:
      yawNow -= servoStep
      if yawNow < yawDest:
        yawNow = yawDest
    pwm.setPWM(0, 0, yawNow + yawAdj)
    sleep (speed * 0.01)

def centering (servoNum=4): # Centering Servos
  pwm.setPWM(0, 0, pulseMid + yawAdj + 10)
  pwm.setPWM(0, 0, pulseMid + yawAdj)
  sleep(0.1)
  pwm.setPWM(1, 0, pulseMid + rotAdj + 10)
  sleep(0.2)
  pwm.setPWM(1, 0, pulseMid + rotAdj)
  sleep(0.1)
  pwm.setPWM(2, 0, pulseMid + pitAdj + 10)
  sleep(0.2)
  pwm.setPWM(2, 0, pulseMid + pitAdj)
  sleep(0.1)
  c = 3
  while c < servoNum:
    pwm.setPWM(c, 0, pulseMid + 10)
    sleep(0.2)
    pwm.setPWM(c, 0, pulseMid)
    sleep(0.1)
    c += 1
