# Bezelie Sample Code for Raspberry Pi : Servo Movement Test

from  time import sleep
import bezelie

# Set Up
bezelie.initPCA9685()

# Main Loop
try:
  while (True):
    bezelie.moveHead (20)
#    bezelie.moveHead (-20)
    bezelie.moveHead (0)
    sleep (0.5)
    bezelie.moveBack (30)
#    bezelie.moveBack (-30)
    bezelie.moveBack (0)
    sleep (0.5)
    bezelie.moveStage (40)
#    bezelie.moveStage (-40)
    bezelie.moveStage (0)
    sleep (0.5)

except KeyboardInterrupt:
  print " Interrupted by Keyboard"
