# -*- coding: utf-8 -*- 
# Bezelie Sample Code for Raspberry Pi : Camera Moving Test

from  time import sleep
import picamera
import bezelie

# Centering All Servos
bezelie.initPCA9685()
bezelie.moveCenter()

# Main Loop
try:
  with picamera.PiCamera() as camera:
    camera.resolution = (800, 480)   # change this number depending on your display
    camera.rotation = 180            # comment out if your screen is upside down
    camera.start_preview()
    sleep(2)
    head = 0
    while (True):
      bezelie.moveBack (20)
      bezelie.moveStage (40, 2)
      sleep (0.5)
      bezelie.moveBack (-20)
      bezelie.moveStage (-40, 2)
      sleep (0.5)
      head += 10
      if head > 20:
        head = -20
      bezelie.moveHead (head)

except KeyboardInterrupt:
  print " Interrupted by Keyboard"
