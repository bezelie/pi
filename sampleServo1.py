# Bezelie Sample Code for Raspberry Pi : Servo Movement Test

from Adafruit_PWM_Servo_Driver import PWM
from  time import sleep

pwm = PWM(0x40)

# Constants
center = 310
pitMin = center - 30 # Upward
pitMax = center + 30 # Downward
rotMin = center - 50 # Clockwise
rotMax = center + 50 # AntiClockwise
yawMin = center -100 # Clocwise
yawMax = center +100 # AntiClockWise
pwm.setPWMFreq(47)   # Set frequency to 50 Hz

# Initialization
pit = pitDest = rot = rotDest = yaw = yawDest = center

# Functions
def servo (speed=0.001):
  global pit, rot, yaw
  while (True):
    if pit < pitDest:
      pit += 1
    if pit > pitDest:
      pit -= 1
    pwm.setPWM(2, 0, pit)
    if rot < rotDest:
      rot += 1
    if rot > rotDest:
      rot -= 1
    pwm.setPWM(1, 0, rot)
    if yaw < yawDest:
      yaw += 1
    if yaw > yawDest:
      yaw -= 1
    pwm.setPWM(0, 0, yaw)
#    sleep (speed)
    if pit == pitDest and rot == rotDest and yaw == yawDest:
      break

# Centering All Servos
c = 0
while c < 16:
    pwm.setPWM(c, 0, center)
    c += 1
    sleep(0.1)

# Main Loop
try:
  while (True):
    pitDest = pitMax
    servo ()
    sleep (0.2)
    pitDest = pitMin
    servo ()
    sleep (0.2)
    pitDest = center
    servo ()
    sleep (0.5)
    rotDest = rotMax
    servo ()
    sleep (0.2)
    rotDest = rotMin
    servo ()
    sleep (0.2)
    rotDest = center
    servo ()
    sleep (0.5)
    yawDest = yawMax
    servo ()
    sleep (0.2)
    yawDest = yawMin
    servo ()
    sleep (0.2)
    yawDest = center
    servo ()
    sleep (0.5)
except KeyboardInterrupt:
  print " Interrupted by Keyboard"

