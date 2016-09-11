#!/usr/bin/python
# Bezelie Sample Code for Raspberry Pi : Looking Around

from Adafruit_PWM_Servo_Driver import PWM
import time
import picamera

pwm = PWM(0x40)

center = 310
yawMin = center-100  # 40 degrees Clocwise
yawMax = center+100  # 40 degrees AntiClockWise
rotMin = center - 30 # 30 degrees Clockwise
rotMax = center + 30 # 30 degrees AntiClockwise
pitchMin = center-20 # 30 degrees Upward
pitchMax = center+10 # 15 degrees Downward
pwm.setPWMFreq(47)   # Set frequency to 50 Hz

d = 0
while d < 16:                       # Centering All Servos
    pwm.setPWM(d, 0, center)
    d += 1
    time.sleep(0.1)

with picamera.PiCamera() as camera:
  camera.resolution = (800, 480) 
  camera.rotation = 180
  camera.start_preview()
  time.sleep(0.5)
  pitch = center
  yaw = center
  ySpeed = 0.01
  while (True):
      pwm.setPWM(1, 0, rotMin)
      while yaw < yawMax:
        pwm.setPWM(0, 0, yaw)
        yaw += 1
        time.sleep(ySpeed)
      pwm.setPWM(1, 0, rotMax)
      while yaw > yawMin:
        pwm.setPWM(0, 0, yaw)
        yaw -= 1
        time.sleep(ySpeed)
      pitch += 5
      if pitch > pitchMax:
        pitch = pitchMin
      pwm.setPWM(2, 0, pitch)
      time.sleep(0.1)
