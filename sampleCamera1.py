# Bezelie Sample Code for Raspberry Pi : Camera Moving Test

from  time import sleep
import picamera
import bezelie

# Centering All Servos
bezelie.centering()
sleep (1)

# Main Loop
try:
  with picamera.PiCamera() as camera:
    camera.resolution = (800, 480)   # change this number depending on your display
    camera.rotation = 180            # comment out if your screen is upside down
    camera.start_preview()
    sleep(2)
    pit = 0
    while (True):
      bezelie.moveRot (-10)
      sleep (0.5)
      bezelie.moveYaw (-40, 2)
      sleep (1)
      bezelie.moveRot ( 10)
      sleep (0.5)
      bezelie.moveYaw (40, 2)
      sleep (1)
      pit += 10
      if pit > 20:
        pit = -20
      bezelie.movePit (pit)
      sleep (0.5)

except KeyboardInterrupt:
  print " Interrupted by Keyboard"
