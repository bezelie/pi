# Bezelie Sample Code for Raspberry Pi : Camera Moving Test

from  time import sleep
import picamera
import bezelie

# Centering All Servos
bezelie.centering()

# Main Loop
try:
  with picamera.PiCamera() as camera:
    camera.resolution = (800, 480)   # Change this number for your display
    camera.rotation = 180            # comment out if your screen upside down
    camera.start_preview()
    sleep(0.2)
    pit = 0
    while (True):
      bezelie.moveRot (-20)
      bezelie.moveYaw (-40, 2)
      sleep (0.1)
      bezelie.moveRot (20)
      bezelie.moveYaw (40, 2)
      sleep (0.1)
      pit += 10
      if pit > 20:
        pit = -30
      bezelie.movePit (pit)

except KeyboardInterrupt:
  print " Interrupted by Keyboard"

GPIO.cleanup()
