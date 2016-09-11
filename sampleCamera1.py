# Bezelie Sample Code for Raspberry Pi : Camera Looking Around

from Adafruit_PWM_Servo_Driver import PWM
from  time import sleep
import picamera

pwm = PWM(0x40)

# Constants
center = 310
pitMin = center - 30 # Upward
pitMax = center + 30 # Downward
rotMin = center - 40 # Clockwise
rotMax = center + 40 # AntiClockwise
yawMin = center -100 # Clocwise
yawMax = center +100 # AntiClockWise
pwm.setPWMFreq(47)   # Set frequency to 50 Hz

# Initialization
pit = yaw = center
pSpeed = 10
ySpeed = 0.01

# Centering All Servos
c = 0
while c < 16:
    pwm.setPWM(c, 0, center)
    c += 1
    sleep(0.1)

# Main Loop
try:
  with picamera.PiCamera() as camera:
    camera.resolution = (800, 480)   # Change this number for your display
    camera.rotation = 180            # comment out if your screen upside down
    camera.start_preview()
    sleep(0.2)
    while (True):
      pwm.setPWM(1, 0, rotMin)
      while yaw < yawMax:
        pwm.setPWM(0, 0, yaw)
        yaw += 1
        sleep(ySpeed)
      pwm.setPWM(1, 0, rotMax)
      while yaw > yawMin:
        pwm.setPWM(0, 0, yaw)
        yaw -= 1
        sleep(ySpeed)
      pit += pSpeed
      if pit > pitMax:
        pit = pitMin
      pwm.setPWM(2, 0, pit)
      sleep(0.1)
except KeyboardInterrupt:
  print " Interrupted by Keyboard"
