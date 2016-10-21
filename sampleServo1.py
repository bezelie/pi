# Bezelie Sample Code for Raspberry Pi : Servo Movement Test

from  time import sleep
import bezelie

# Set Up
bezelie.centering()

# Main Loop
try:
  while (True):
    bezelie.movePit (30, 2)
    sleep (0.2)

    bezelie.movePit (-30, 1)
    sleep (0.2)

    bezelie.movePit (0)
    sleep (0.5)

    bezelie.moveRot (30, 1)
    sleep (0.2)

    bezelie.moveRot (-30, 1)
    sleep (0.2)

    bezelie.moveRot (0)
    sleep (0.5)

    bezelie.moveYaw (40)
    sleep (0.2)

    bezelie.moveYaw (-40)
    sleep (0.2)

    bezelie.moveYaw (0)
    sleep (0.5)

except KeyboardInterrupt:
  print " Interrupted by Keyboard"
