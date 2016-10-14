# Bezelie Sample Code for Raspberry Pi : Camera Moving Test

from  time import sleep
import picamera
import bezelie

# Centering All Servos
bezelie.centering()

# Main Loop
try:
  with picamera.PiCamera() as camera:
    camera.resolution = (800, 480)   # change this number depending on your display
    camera.rotation = 180            # comment out if your screen is upside down
    camera.start_preview()
    sleep(0.2)
    pit = 0
    while (True):
      bezelie.moveRot (-20)
      bezelie.moveYaw (-40, 2)
      sleep (1)
      bezelie.moveRot (20)
      bezelie.moveYaw (40, 2)
      sleep (1)
      pit += 10
      if pit > 20:
        pit = -20
      bezelie.movePit (pit)
      sleep (1)

except KeyboardInterrupt:
  print " Interrupted by Keyboard"
